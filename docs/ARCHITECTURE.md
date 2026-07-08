# Drone Swarm Framework Architecture Specification

## 1. Project Vision
The Drone Swarm Framework is a lightweight, modular system designed to orchestrate autonomous UAV swarms. The core vision is to provide a robust foundation for complex swarm behaviors—including formation flight, synchronized movement, and autonomous missions—while maintaining a clear separation between high-level intent and low-level hardware execution.

## 2. Architectural Principles
*   **Domain-Driven Design:** System capabilities are partitioned into distinct, cohesive domains (Mission, Formation, Planning, Safety).
*   **Unidirectional Dependencies:** Dependencies strictly flow from high-level orchestrators (SystemCoordinator, Mission) to low-level executors (SwarmManager, Drone), eliminating circular dependencies.
*   **Separation of Concerns:** Intent (Mission) is decoupled from Geometry (Formation), which is decoupled from Movement Math (Planning) and Constraints (Safety).
*   **Registry-Based Orchestration:** Active instances (missions, formations) are managed via registries within a SystemCoordinator, enabling concurrency and dynamic reconfiguration.
*   **Dual Data Flows:** Execution flow (request/response orchestration) is explicitly separated from the Observation flow (event-driven telemetry).

## 3. Existing Infrastructure
Infrastructure modules are treated as foundational support services:
*   `CLI`/`Commands`: Interface layer.
*   `Telemetry`: State observation service.
*   `Messaging`: Asynchronous event bus.
*   `SwarmManager`: Low-level executor (MAVLink abstraction).
*   `Drone`: Hardware-level interface.
*   `Config`: System-wide configuration.
## 4. Domain Architecture
The architecture is structured around six primary domains:
1.  **SystemCoordinator:** Orchestrates interactions between domains.
2.  **Execution:** Manages runtime state of validated plans.
3.  **Mission:** Owns swarm objectives, sequencing, and lifecycle.
4.  **Formation:** Owns spatial organization (geometry, offsets).
5.  **Planning:** Owns spatial primitives (Waypoints, Trajectories, ExecutionPlans) and pure mathematical utilities for geographic and coordinate transforms.
6.  **Safety:** Owns constraint validation (geofence, collision, execution validation).

### Execution Domain Structure
* `api.py`: Public Interface for execution session lifecycle management.
* `manager.py`: Runtime state orchestration and progress tracking.
* `registry.py`: Internal storage for active execution sessions.
* `models.py`: Mutable runtime data schemas (ExecutionSession, ExecutionStatus).
* `events.py`: Domain-owned events.
* `exceptions.py`: Domain-specific exceptions.

### SystemCoordinator Domain Structure
* `api.py`: Public Interface for orchestration (session, loading, plan building).
* `manager.py`: Session state orchestration.
* `models.py`: Data schemas (CoordinatorSession).
* `exceptions.py`: Domain-specific exceptions.

### Mission Domain Structure
* `api.py`: Public Interface for mission management (lifecycle, sequencing).
* `manager.py`: Mission state orchestration.
* `executor.py`: Mission progress tracking and goal advancement.
* `planner.py`: Mission sequencing logic.
* `registry.py`: Internal storage for active missions.
* `models.py`: Immutable data schemas (Mission, MissionGoal, MissionPlan, MissionProgress).
* `types.py`: Enums (MissionType, MissionStatus).
* `events.py`: Domain-owned events.
* `exceptions.py`: Domain-specific exceptions.

### Formation Domain Structure
...

1. **Formation State:** The `Formation` model maintains configuration (type, leader, followers, spacing).
2. **Geometry Generation:** `generate_offsets()` calculates relative `Position` offsets for all drones in the formation.
3. **Planning Delegation:** The `planner.py` module iterates through offsets and calls `Planning.api.offset_waypoint()` to convert relative offsets into absolute `Waypoint` targets based on a given leader `Waypoint`.
4. **Safety Validation:** Final generated `ExecutionPlan` targets must pass `Safety.api.validate_execution_plan()` before being utilized for command dispatch.

* **Ownership:**
  * `Formation` owns relative geometry.
  * `Planning` owns absolute coordinate conversion.
  * `SwarmManager` owns final command execution.
  * `Mission` owns swarm sequencing.

### Safety Domain Structure
* `api.py`: Public Interface for plan validation and constraint management.
* `registry.py`: Internal registry for managing active constraints.
* `models.py`: Data schemas (Constraint, SafetyResult, SafetyViolation).
* `validators.py`: Stateless validation logic.
* `events.py`: Domain-owned events.
* `exceptions.py`: Domain-specific exceptions.

## 5. Ownership Matrix
| Concept | Primary Owner |
| :--- | :--- |
| Mission / Mission State | `Mission` |
| Formation / Assignment | `Formation` |
| Waypoint / Route / ExecutionPlan | `Planning` |
| Constraints / Validation | `Safety` |
| Drone State | `Drone` |
| Telemetry Data | `Telemetry` |
| User Requests | `Commands` / `SystemCoordinator` |

## 6. Dependency Graph
```text
[SystemCoordinator]
    ↓
[MissionManager]
    ↓
[FormationManager]
    ↓
[Planning]
    ↓
[Safety]
    ↓
[SwarmManager]
    ↓
[Drone] / [Telemetry] / [Messaging]
```

## 7. Execution Flow
Request-Response orchestration (Orchestrated by SystemCoordinator):
`CLI` → `Parser` → `Validator` → `Dispatcher` → `Handlers` → `SystemCoordinator.orchestrate_mission()` → [`Mission` → `Formation` → `Planning` → `Safety` → `Execution`] → `ExecutionSession`

## 8. Observation Flow
Asynchronous Event Pub-Sub:
`Drone` → `Telemetry` → `Messaging` → [`Mission`, `Formation`, `Safety`, `UI`]

## 9. Domain Contracts
All domains expose a single `api.py` as their public interface. Internal logic is strictly encapsulated within an `internal/` directory and must not be imported across domain boundaries.

## 10. Folder Structure
```text
<domain>/
├── api.py           # Public Interface
├── registry.py      # Internal Instance Registry
├── models.py        # Data Schemas (DTOs)
├── events.py        # Domain-owned Events
├── exceptions.py    # Domain-specific Errors
└── internal/        # Private Implementation Details
```

## 11. Public APIs
*   **Mission:** `create_mission()`, `start()`, `pause()`, `cancel()`
*   **Formation:** `set_type()`, `set_leader()`, `assign_follower()`
*   **Planning:** `generate_plan()`, `transform_coords()`
*   **Safety:** `validate_execution_plan()`, `register_constraint()`, `unregister_constraint()`, `list_constraints()`

## 12. Import Rules
Domains must import only their immediate subordinates in the dependency graph. Imports from `CLI`, `Drone`, or `Telemetry` are forbidden within domain logic.

## 13. Registry Responsibilities
*   **MissionRegistry:** Stores `MissionInstance` state (Active/Paused).
*   **FormationRegistry:** Stores `FormationInstance` state.
*   Registries are managed by the `SystemCoordinator`.

## 14. Planner Responsibilities
*   **MissionPlanner:** Maps high-level goals into a sequence of Formation goals.
*   **FormationPlanner:** Maps Formation goals into specific spatial configurations.
*   **Planning Domain:** Owns `ExecutionPlan` construction, trajectory generation, and geographic/coordinate mathematics. It provides reusable services for route manipulation, validation, and planning primitive generation.

## 15. Event Ownership
*   **Mission:** `MissionStarted`, `MissionPaused`
*   **Formation:** `FormationChanged`
*   **Planning:** `ExecutionPlanGenerated`
*   **Safety:** `SafetyViolation`

## 16. Error Ownership
*   `MissionError`, `FormationError`, `PlanningError`, `SafetyViolation`, `ExecutionError`.

## 17. Future Extensibility
*   **Heterogeneous UAVs:** Handled by `Planning` utilizing platform-specific capability profiles.
*   **Obstacle Avoidance:** Integrated via new checkers in `Safety.internal`.
*   **Swarm Splitting:** `SystemCoordinator` creates/deletes instances in `FormationRegistry`.

## 18. Architectural Constraints
*   No circular imports.
*   No domain-level code in infrastructure modules.
*   `SystemCoordinator` delegates; it does not manage domain state.

## 19. Implementation Roadmap
1.  **Phase 1 (Navigation & Safety Primitives):** Implementation of `Planning` and `Safety` domains.
2.  **Phase 2 (Formation Engine):** Implementation of `Formation` domain.
3.  **Phase 3 (Mission Sequencing):** Implementation of `Mission` domain.
4.  **Phase 4 (Obstacle Avoidance):** Implementation of advanced `Safety` constraints.

## 20. Architecture Decision Summary
*   Registries are localized for concurrency.
*   Dual flows (Execution/Observation) are enforced.
*   Unidirectional dependencies are strict.
*   Planning owns spatial primitives.
*   **Status Update:** The Planning, Safety, and Formation domains are now fully implemented, tested, and frozen (v1.0).

---

## Architecture Status
*   **Architecture Version:** 1.0.0
*   **Current Phase:** Phase 1
*   **Current Milestone:** Formation Domain Frozen
*   **Architecture Frozen:** Yes
*   **Date Updated:** 2026-07-07
