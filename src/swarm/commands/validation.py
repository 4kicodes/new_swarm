from typing import Dict, Tuple
from .models import Command

# Command: (min_args, max_args, usage)
COMMAND_SPECS: Dict[str, Tuple[int, int, str]] = {
    "arm": (0, 0, "arm <target>"),
    "mode": (1, 1, "mode <target> <mode>"),
    "takeoff": (1, 1, "takeoff <target> <meters>"),
    "land": (0, 0, "land <target>"),
    "help": (0, 0, "help"),
}

def validate(command: Command):
    """Validates command structure."""
    if not command.name:
        return
        
    if command.name in ["exit", "quit"]:
        return

    if command.name not in COMMAND_SPECS:
        raise ValueError("Unknown command.")
        
    min_args, max_args, usage = COMMAND_SPECS[command.name]
    
    # Check target
    if command.name != "help" and not command.target:
        raise ValueError(f"Usage:\n{usage}")
        
    # Check args
    if not (min_args <= len(command.args) <= max_args):
        raise ValueError(f"Usage:\n{usage}")
        
    # Validate numeric args
    if command.name == "takeoff":
        try:
            float(command.args[0])
        except ValueError:
            raise ValueError("Altitude must be numeric.")
