import math
from panda3d.core import NodePath, Vec3
from direct.task import Task
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class SimpleCircleOrbitTask:
    orbitTimer = 0

    def __init__(
        self,
        base: SpaceJamBase,
        orbiter_node: NodePath,
        orbiting_around_node: NodePath,
        orbit_duration: float,
        # Orbit Type is based on frame of orbiting_around_node.
        orbit_type: int,  # 0 = XY, 1 = XZ, 2 = YZ
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

    def startOrbiting(self):
        self.taskMgr.add(self.orbitTask, self.orbitTaskName)

    def stopOrbiting(self):
        self.taskMgr.remove(self.orbitTaskName)

    def _updateCurrPosForOrbit(self):
        # Current orbit timer divided by duration is where in the orbit we currently are.
        # print( "RADIUS = " + str(self.orbitRadius) + "; ORBIT = " + str(self.orbitTimer / self.orbitDuration) )
        theta = (self.orbitTimer * 2 * math.pi) / self.orbitDuration

        # Set exact position based on orbit type
        if self.orbitType == 0:  # XY
            currPos = Vec3(math.sin(theta), math.cos(theta), 0) * self.orbitRadius
        elif self.orbitType == 1:  # XZ
            currPos = Vec3(math.cos(theta), 0, math.sin(theta)) * self.orbitRadius
        elif self.orbitType == 2:  # YZ
            currPos = Vec3(0, math.cos(theta), math.sin(theta)) * self.orbitRadius
        else:  # XY is the default; copied from type 0 case.
            currPos = Vec3(math.sin(theta), math.cos(theta), 0) * self.orbitRadius

        self.orbiter.setPos(currPos)

    def getDurationOfType(self, type: int):
        if type == 0:
            # Type 1 starts at a position which is 1/4 of the way through orbit 0
            return self.orbitDuration * 1.25
        elif type == 1:
            return self.orbitDuration * 1.25

        return self.orbitDuration

    def getStartTimerValueForNextType(self, currDuration: float):
        if self.orbitType == 1:
            return self.getDurationOfType(2) * 0.25

        return self.orbitTimer - currDuration

    def _updateOrbitTimerAndType(self):
        # Add "Delta Time" (time since last game update) seconds to orbitTimer
        self.orbitTimer += self.gClock.getDt()

        # Some orbit types start in different positions so for some transitions we want more than one cycle
        currDuration = self.getDurationOfType(self.orbitType)

        if self.orbitTimer >= currDuration:
            # If orbitTimer is too big, we subtract duration to wrap it back down.
            self.orbitTimer = self.getStartTimerValueForNextType(currDuration)
            self.orbitType = self.orbitType + 1
            if self.orbitType >= 3:
                self.orbitType = 0
            print("Orbiter changed type! Is now type " + str(self.orbitType))

    def orbitTask(self, task: Task):
        self._updateOrbitTimerAndType()
        self._updateCurrPosForOrbit()

        if self.lookAtOrbited == True:
            self.orbiter.lookAt(
                self.orbiting,
                self.orbiting.parent.getRelativeVector(self.orbiting, (0, 1, 0)),
            )

        return task.cont
