from typing import Optional
from .models import Mission, MissionProgress, MissionGoal
from .planner import MissionPlanner
from .types import MissionStatus

class MissionExecutor:
    def __init__(self, mission: Mission):
        self.mission = mission
        self.progress = MissionProgress(
            remaining_goals=[g.goal_id for g in (mission.plan.goals if mission.plan else [])]
        )

    def current_goal(self) -> Optional[MissionGoal]:
        if not self.has_next_goal():
            return None
        goal_id = self.progress.remaining_goals[0]
        for goal in self.mission.plan.goals:
            if goal.goal_id == goal_id:
                return goal
        return None

    def has_next_goal(self) -> bool:
        return len(self.progress.remaining_goals) > 0

    def advance_goal(self) -> None:
        if self.has_next_goal():
            goal_id = self.progress.remaining_goals.pop(0)
            self.progress.completed_goals.append(goal_id)
            self.progress = MissionProgress(
                current_goal_index=self.progress.current_goal_index + 1,
                completed_goals=self.progress.completed_goals,
                remaining_goals=self.progress.remaining_goals,
                status=MissionStatus.RUNNING
            )

    def mission_complete(self) -> bool:
        return not self.has_next_goal() and self.progress.status == MissionStatus.RUNNING
