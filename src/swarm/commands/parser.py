from typing import List
from .models import Command

def parse(line: str) -> Command:
    """Parses raw text into a Command object."""
    tokens = line.strip().split()
    if not tokens:
        return Command(name="")
    
    name = tokens[0].lower()
    
    if len(tokens) == 1:
        return Command(name=name)
        
    # Simple logic: assume tokens[1] is target, rest are args
    return Command(
        name=name,
        target=tokens[1],
        args=tokens[2:]
    )
