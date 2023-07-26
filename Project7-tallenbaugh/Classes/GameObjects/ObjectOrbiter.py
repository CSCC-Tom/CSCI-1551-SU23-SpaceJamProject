import math
from panda3d.core import NodePath, ClockObject, Vec3
from direct.task import Task
from direct.task.Task import TaskManager


class ObjectOrbiter:
    orbitTimer = 0

    def __init__(
        self,
        orbiter_node: NodePath,
        orbiting_around_node: NodePath,
        global_clock: ClockObject,
        task_manager: TaskManager,
        orbit_duration: float,
        # Orbit Type is based on frame of orbiting_around_node.
        orbit_type: int,  # 0 = XY, 1 = XZ, 2 = YZ
        look_at_orbited: bool = False,
    ):
        self.orbiter = orbiter_node
        self.orbiting = orbiting_around_node
        self.taskMgr = task_manager
        self.orbitTaskName = self.orbiter.name + "-orbits-" + self.orbiting.name
        self.orbitDuration = orbit_duration
        self.gClock = global_clock
        self.orbitType = orbit_type
        self.orbitRadius = orbiter_node.get_distance(orbiting_around_node) * 14
        self.lookAtOrbited = look_at_orbited

    def startOrbiting(self):
        self.taskMgr.add(self.orbitTask, self.orbitTaskName)

    def stopOrbiting(self):
        self.taskMgr.remove(self.orbitTaskName)

    def CircleXY(
        self, time: float, numSeams: int, radius: float = 1, duration: float = 1
    ):
        theta = (time / numSeams * 2 * math.pi) / duration
        return Vec3(math.sin(theta), math.cos(theta), 0) * radius

    def orbitTask(self, task: Task):
        self.orbitTimer += self.gClock.getDt()
        if self.orbitTimer >= self.orbitDuration:
            # If orbitTimer is too big, we subtract duration to wrap it back down.
            self.orbitTimer -= self.orbitDuration

        # Current orbit timer divided by duration is where in the orbit we currently are.
        # print( "RADIUS = " + str(self.orbitRadius) + "; ORBIT = " + str(self.orbitTimer / self.orbitDuration) )
        self.orbiter.setPos(
            self.CircleXY(self.orbitTimer, 1, self.orbitRadius, self.orbitDuration)
        )
        if self.lookAtOrbited == True:
            self.orbiter.lookAt(
                self.orbiting,
                self.orbiting.parent.getRelativeVector(self.orbiting, (0, 1, 0)),
            )

        return task.cont
