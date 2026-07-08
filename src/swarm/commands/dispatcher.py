from . import handlers
from . import coordinator_handlers

HANDLERS = {
    "arm": handlers.arm,
    "mode": handlers.mode,
    "takeoff": handlers.takeoff,
    "land": handlers.land,
    "help": handlers.help_handler,
    # Coordinator handlers
    "create_mission": coordinator_handlers.create_mission,
    "load_mission": coordinator_handlers.load_mission,
    "create_formation": coordinator_handlers.create_formation,
    "load_formation": coordinator_handlers.load_formation,
    "set_leader": coordinator_handlers.set_leader,
    "set_followers": coordinator_handlers.set_followers,
    "set_spacing": coordinator_handlers.set_spacing,
    "set_type": coordinator_handlers.set_type,
    "generate_plan": coordinator_handlers.generate_execution_plan,
}

async def dispatch(manager, command):
    if command.name in HANDLERS:
        await HANDLERS[command.name](manager, command)
