import math
from enum import Enum
from panda3d.core import NodePath, Vec3
from direct.task import Task
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class OrbitType(Enum):
    XY = 0
    XZ = 1
    YZ = 2


class SimpleCircleOrbitTask:
    """Sets orbit radius to be based on the starting distance between the nodes"""

    orbitTimer = 0

    def __init__(
        self,
        base: SpaceJamBase,
        orbiter_node: NodePath,
        orbiting_around_node: NodePath,
        orbit_duration: float,
        start_immediately: bool = True,
        # Orbit Type is based on frame of orbiting_around_node.
        orbit_type: OrbitType = OrbitType.XY,
        look_at_orbited: bool = False,
    ):
        self.orbiter = orbiter_node
        self.orbiting = orbiting_around_node
        self.taskMgr = base.taskMgr
        self.orbitTaskName = self.orbiter.name + "-orbits-" + self.orbiting.name
        self.orbitDuration = orbit_duration
        self.gClock = base.clock
        self.orbitType = orbit_type
        self.orbitRadius = orbiter_node.get_distance(orbiting_around_node) * 14
        self.lookAtOrbited = look_at_orbited
        if start_immediately == True:
            self.startOrbiting()

    def startOrbiting(self):
        self.taskMgr.add(self.orbitTask, self.orbitTaskName)

    def stopOrbiting(self):
        self.taskMgr.remove(self.orbitTaskName)

    def updateCurrPosForOrbit(self):
        # Current orbit timer divided by duration is where in the orbit we currently are.
        # print( "RADIUS = " + str(self.orbitRadius) + "; ORBIT = " + str(self.orbitTimer / self.orbitDuration) )
        theta = (self.orbitTimer * 2 * math.pi) / self.orbitDuration

        # Set exact position based on orbit type
        if self.orbitType == OrbitType.XY:
            currPos = Vec3(math.sin(theta), math.cos(theta), 0) * self.orbitRadius
        elif self.orbitType == OrbitType.XZ:
            currPos = Vec3(math.cos(theta), 0, math.sin(theta)) * self.orbitRadius
        elif self.orbitType == OrbitType.YZ:
            currPos = Vec3(0, math.cos(theta), math.sin(theta)) * self.orbitRadius
        else:  # XY is the default; copied from type 0 case.
            currPos = Vec3(math.sin(theta), math.cos(theta), 0) * self.orbitRadius

        self.orbiter.setPos(currPos)

        if self.lookAtOrbited == True:
            self.orbiter.lookAt(
                self.orbiting,
                self.orbiting.parent.getRelativeVector(self.orbiting, (0, 1, 0)),
            )

    def updateOrbitTimer(self):
        # Add "Delta Time" (time since last game update) seconds to orbitTimer
        self.orbitTimer += self.gClock.getDt()

    def orbitTask(self, task: Task):
        self.updateOrbitTimer()
        self.updateCurrPosForOrbit()

        return task.cont


class DynamicCircleOrbitTask(SimpleCircleOrbitTask):
    """Logic wrapped around SimpleCircleOrbitTask that will go through all the orbits over time."""

    def __init__(
        self,
        base: SpaceJamBase,
        orbiter_node: NodePath,
        orbiting_around_node: NodePath,
        orbit_duration: float,
        start_immediately: bool = True,
    ):
        SimpleCircleOrbitTask.__init__(
            self,
            base,
            orbiter_node,
            orbiting_around_node,
            orbit_duration,
            start_immediately,
            OrbitType.XY,
            False,
        )

    def getDurationOfType(self, type: OrbitType):
        if type == OrbitType.XY:
            # Type 1 starts at a position which is 1/4 of the way through orbit 0
            return self.orbitDuration * 1.25
        elif type == OrbitType.XZ:
            return self.orbitDuration * 1.25
        # OrbitType.YZ
        return self.orbitDuration

    def getNextTypeFor(self, type: OrbitType):
        if type == OrbitType.XY:
            return OrbitType.XZ
        elif type == OrbitType.XZ:
            return OrbitType.YZ
        else:  # type == OrbitType.YZ
            return OrbitType.XY

    def getStartTimerValueForNextType(self, currDuration: float):
        if self.orbitType == OrbitType.XZ:
            return self.getDurationOfType(self.getNextTypeFor(OrbitType.XZ)) * 0.25

        return self.orbitTimer - currDuration

    def updateOrbitTimer(self):
        SimpleCircleOrbitTask.updateOrbitTimer(self)

        # Some orbit types start in different positions so for some transitions we want more than one cycle
        currDuration = self.getDurationOfType(self.orbitType)

        if self.orbitTimer >= currDuration:
            # If orbitTimer is too big, we subtract duration to wrap it back down.
            self.orbitTimer = self.getStartTimerValueForNextType(currDuration)
            self.orbitType = self.getNextTypeFor(self.orbitType)
            print("Orbiter changed type! Is now type " + str(self.orbitType))
