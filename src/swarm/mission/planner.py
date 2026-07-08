from typing import List
from .models import MissionPlan, MissionGoal

class MissionPlanner:
    @staticmethod
    def get_execution_order(plan: MissionPlan) -> List[MissionGoal]:
        """Returns the ordered list of mission goals."""
        return plan.goals
