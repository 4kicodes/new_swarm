import asyncio
from swarm import commands

async def run_repl(manager):
    """Command REPL using the new asynchronous pipeline."""
    print("Drone Swarm Framework REPL (Async). Type 'exit' to quit.")
    
    loop = asyncio.get_running_loop()
    
    while True:
        try:
            # Use run_in_executor to avoid blocking the event loop (compatible with Python 3.8+)
            line = await loop.run_in_executor(None, input, "swarm > ")
            if not line.strip(): continue
            
            command = commands.parse(line)
            
            if command.name in ["exit", "quit"]:
                break
                
            commands.validate(command)
            
            # Await the dispatch as it is now async
            await commands.dispatch(manager, command)
            
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Error: {e}")
        except (EOFError, KeyboardInterrupt):
            break
