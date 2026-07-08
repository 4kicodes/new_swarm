"""
Drone-specific exception definitions.
"""

# Re-export built-in exceptions or define specific ones only if absolutely necessary.
# In this framework, standard exceptions suffice.
class DroneConnectionError(RuntimeError):
    """Raised when a connection to a drone cannot be established."""
