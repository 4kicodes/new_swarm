import asyncio
from swarm.config.config import load_config
from swarm.drone.manager import SwarmManager
from swarm.messaging.bus import InMemoryBus
from swarm.messaging.monitors.health_monitor import HealthMonitor
from swarm.cli.app import run_repl
from loguru import logger

async def async_main():
    config = load_config()
    bus = InMemoryBus()

    # Initialize Health Monitor (Subscriber)
    health_monitor = HealthMonitor(bus)

    # Initialize Swarm Manager
    manager = SwarmManager(config, bus)

    logger.info("Initializing swarm connections...")
    await manager.connect_all()
    
    if not manager.connections:
        logger.error("No drones connected. Exiting.")
        return

    # Start CLI REPL
    try:
        await run_repl(manager)
    finally:
        logger.info("Disconnecting from swarm...")
        await manager.disconnect_all()

def main():
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
