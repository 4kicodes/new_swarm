import asyncio
from swarm.drone.connection import DroneConnection
from swarm.messaging.bus import InMemoryBus
from loguru import logger

class SwarmManager:
    def __init__(self, config, bus: InMemoryBus):
        self.config = config
        self.bus = bus
        self.connections = {}  # drone_id -> DroneConnection

    async def connect_all(self):
        tasks = []
        for endpoint in self.config["mavlink"]["endpoints"]:
            conn = DroneConnection(
                connection_string=endpoint,
                bus=self.bus,
                wait_ready=self.config["connection"]["wait_ready"],
                heartbeat_timeout=self.config["connection"]["heartbeat_timeout"],
            )
            tasks.append(self._connect_and_register(conn))
        
        await asyncio.gather(*tasks)

    async def _connect_and_register(self, conn: DroneConnection):
        try:
            await conn.connect()
            drone_id = conn.identity
            self.connections[drone_id] = conn
            logger.success(f"Connected {drone_id} at {conn.connection_string}")
        except Exception as e:
            logger.error(f"Failed to connect/register {conn.connection_string}: {e}")

    def get_drones(self):
        """Returns a dict of drone_id -> Vehicle instance"""
        # Note: This returns the underlying DroneKit vehicle, which might be accessed synchronously.
        # This is a potential future bottleneck, but keeping it for now to minimize refactor impact.
        return {drone_id: conn.vehicle for drone_id, conn in self.connections.items()}

    def get_drone(self, drone_id: str) -> DroneConnection:
        if drone_id not in self.connections:
            raise ValueError(f"Drone {drone_id} not connected.")
        return self.connections[drone_id]

    async def arm(self, drone_id: str):
        await self.get_drone(drone_id).arm()

    async def arm_all(self):
        await asyncio.gather(*(conn.arm() for conn in self.connections.values()))

    async def set_mode(self, drone_id: str, mode_name: str):
        await self.get_drone(drone_id).set_mode(mode_name)

    async def set_mode_all(self, mode_name: str):
        await asyncio.gather(*(conn.set_mode(mode_name) for conn in self.connections.values()))

    async def takeoff(self, drone_id: str, altitude: float):
        await self.get_drone(drone_id).takeoff(altitude)

    async def takeoff_all(self, altitude: float):
        await asyncio.gather(*(conn.takeoff(altitude) for conn in self.connections.values()))

    async def land(self, drone_id: str):
        await self.get_drone(drone_id).land()

    async def land_all(self):
        await asyncio.gather(*(conn.land() for conn in self.connections.values()))

    async def disconnect_all(self):
        await asyncio.gather(*(conn.disconnect() for conn in self.connections.values()))
