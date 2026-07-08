from swarm import coordinator
from swarm.mission import MissionType
from swarm.formation import FormationType
from swarm.planning import create_waypoint

async def create_mission(manager, command):
    # target: m_id, args: [name, type]
    m_id, name, m_type = command.target, command.args[0], command.args[1]
    coordinator.create_mission(m_id, name, MissionType[m_type.upper()])

async def load_mission(manager, command):
    # target: m_id, args: []
    coordinator.load_mission(command.target)

async def create_formation(manager, command):
    # target: f_id, args: [name, type]
    f_id, name, f_type = command.target, command.args[0], command.args[1]
    coordinator.create_formation(f_id, name, FormationType[f_type.upper()])

async def load_formation(manager, command):
    # target: f_id, args: []
    coordinator.load_formation(command.target)

async def set_leader(manager, command):
    # target: formation_id, args: [leader_id]
    coordinator.set_leader(command.target, command.args[0])

async def set_followers(manager, command):
    # target: formation_id, args: [ids...]
    coordinator.set_followers(command.target, command.args)

async def set_spacing(manager, command):
    # target: formation_id, args: [spacing]
    coordinator.set_spacing(command.target, float(command.args[0]))

async def set_type(manager, command):
    # target: formation_id, args: [type]
    coordinator.set_type(command.target, FormationType[command.args[0].upper()])

async def generate_execution_plan(manager, command):
    # args: [lat, lon, alt]
    wp = create_waypoint(float(command.args[0]), float(command.args[1]), float(command.args[2]))
    plan = coordinator.generate_execution_plan(wp)
    print(f"Plan generated: {plan}")
