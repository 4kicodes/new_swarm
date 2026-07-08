"""
DroneKit connection management.

This module is responsible for establishing and managing a connection
to a single MAVLink vehicle asynchronously.
"""

from __future__ import annotations
import asyncio
import functools
import logging
from dronekit import Vehicle, connect, VehicleMode
from loguru import logger

from swarm.messaging.bus import InMemoryBus
from swarm.messaging.events import ConnectionEvent
from swarm.messaging.topics import TOPIC_DRONE_CONNECTION
from swarm.drone.exceptions import DroneConnectionError

# Suppress noisy heartbeat warnings from DroneKit
logging.getLogger('dronekit').setLevel(logging.ERROR)

class DroneConnection:
    """
    Manages a single DroneKit connection asynchronously.
    """

    def __init__(
        self,
        connection_string: str,
        bus: InMemoryBus,
        wait_ready: bool = True,
        heartbeat_timeout: int = 30,
    ) -> None:

        self._connection_string = connection_string
        self._bus = bus
        self._wait_ready = wait_ready
        self._heartbeat_timeout = heartbeat_timeout

        self._vehicle: Vehicle | None = None
        self._identity: str | None = None

    @property
    def connection_string(self) -> str:
        return self._connection_string

    @property
    def identity(self) -> str:
        if self._identity is None:
            raise RuntimeError("No active drone identity.")
        return self._identity

    @property
    def vehicle(self) -> Vehicle:
        if self._vehicle is None:
            raise RuntimeError("No active vehicle connection.")
        return self._vehicle

    def is_connected(self) -> bool:
        return self._vehicle is not None

    async def connect(self) -> Vehicle:
        if self._vehicle is not None:
            logger.warning("Already connected to {}", self._connection_string)
            return self._vehicle

        logger.info("Connecting to {} (wait_ready=False)...", self._connection_string)

        loop = asyncio.get_running_loop()
        try:
            # Running blocking connect in executor
            self._vehicle = await loop.run_in_executor(
                None,
                functools.partial(connect, self._connection_string, wait_ready=False, heartbeat_timeout=self._heartbeat_timeout)
            )

            # Manual initialization check - use async sleep
            start = asyncio.get_event_loop().time()
            while not self._vehicle.version:
                if asyncio.get_event_loop().time() - start > self._heartbeat_timeout:
                    raise RuntimeError(
                        f"Timed out waiting for vehicle initialization "
                        f"on {self._connection_string}"
                    )
                await asyncio.sleep(0.5)
            
            # Extract Identity
            self._identity = f"drone_{self._vehicle._master.target_system}"
            self._bus.publish(TOPIC_DRONE_CONNECTION, ConnectionEvent(drone_id=self._identity, status="connected"))

        except Exception as exc:
            logger.exception("Connection failed: {}", self._connection_string)
            raise DroneConnectionError(f"Failed to connect to {self._connection_string}") from exc

        logger.success("Connected to {}", self._connection_string)
        return self._vehicle

    async def arm(self):
        """Arm the vehicle."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, setattr, self.vehicle, 'armed', True)

    async def set_mode(self, mode_name: str):
        """Set the vehicle mode."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, setattr, self.vehicle, 'mode', VehicleMode(mode_name.upper()))

    async def takeoff(self, altitude: float):
        """Takeoff the vehicle."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.vehicle.simple_takeoff, altitude)

    async def land(self):
        """Land the vehicle."""
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, setattr, self.vehicle, 'mode', VehicleMode("LAND"))

    async def disconnect(self) -> None:
        """Close the DroneKit connection."""
        if self._vehicle is None:
            return

        logger.info("Disconnecting {}", self._connection_string)
        drone_id = self._identity if self._identity else "unknown"

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._vehicle.close)

        self._vehicle = None
        self._bus.publish(TOPIC_DRONE_CONNECTION, ConnectionEvent(drone_id=drone_id, status="disconnected"))
        logger.success("Disconnected {}", self._connection_string)
