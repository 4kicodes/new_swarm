from .target import resolve_targets

async def arm(manager, command):
    for t in resolve_targets(manager, command.target):
        await manager.arm(t)

async def mode(manager, command):
    mode_name = command.args[0]
    for t in resolve_targets(manager, command.target):
        await manager.set_mode(t, mode_name)

async def takeoff(manager, command):
    altitude = float(command.args[0])
    for t in resolve_targets(manager, command.target):
        await manager.takeoff(t, altitude)

async def land(manager, command):
    for t in resolve_targets(manager, command.target):
        await manager.land(t)

async def help_handler(manager, command):
    print("""
arm <target>
mode <target> <mode>
takeoff <target> <meters>
land <target>
help
exit/quit
""")
