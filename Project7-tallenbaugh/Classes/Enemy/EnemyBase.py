from panda3d.core import NodePath, Vec3, LColor, CollisionNode
from Classes.GameObjects.GameModel import ModelObject
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.GameObjects.ModelWithCollider import (
    ModelWithCapsuleCollider,
)
from Classes.Gameplay.OrbitingLogic import OrbitType, SimpleCircleOrbitTask
from Classes.Enemy.EnemyDrone import EnemyBaseDrone
from Classes.Enemy.EnemyTravelDrone import EnemyTravelDrone


def CreateLinePatternPositionsList(count: int, origin: Vec3, direction: Vec3):
    """Creates a line of count positions starting from the origin and spaced out by the direction vector."""
    pos_list: list[Vec3] = []
    for i in range(count):
        pos_list.append(origin + (direction[0] * i, direction[1] * i, direction[2] * i))
    return pos_list


# dir_a is the direction of each line, dir_b is the direction of each line's subsequent origin.
def CreateLineOfLinePatternsPositionsList(
    count_of_lines: int,
    count_per_line: int,
    origin: Vec3,
    dir_of_each_line: Vec3,
    dir_between_line_origins: Vec3,
):
    """Creates count_of_lines lines each containing count_per_line positions. Each line points towards dir_of_each_line. Each line is dir_between_line_origins apart."""
    pos_list: list[Vec3] = []
    for i in range(count_of_lines):
        line_origin = origin + (
            dir_between_line_origins[0] * i,
            dir_between_line_origins[1] * i,
            dir_between_line_origins[2] * i,
        )
        pos_list.extend(
            CreateLinePatternPositionsList(
                count_per_line, line_origin, dir_of_each_line
            )
        )
    return pos_list


class SpaceJamEnemyBase(ModelWithCapsuleCollider):
    """SphereCollidableObject that also manages a swarm of Defenders"""

    dronesDestroyed = 0

    def __init__(
        self,
        base: SpaceJamBase,
        base_name: str,
        pos: Vec3,
        orbit_around: NodePath,
    ):
        ModelWithCapsuleCollider.__init__(
            self,
            base,
            "./Assets/Universe/Universe.obj",
            base.render,
            base_name,
            (0, 0, 0),
            (0.75, 0, 0),
        )
        self.baseModelB = ModelObject(
            base.loader,
            "./Assets/Universe/Universe.obj",
            self.modelNode,
            base_name + "B",
        )
        self.baseModelB.modelNode.setPos((0.75, 0, 0))
        self.modelNode.setPos(pos)
        self.modelNode.setScale(1.5)

        self.defenders: list[EnemyBaseDrone] = []
        self.spawnDefenders(base, self.modelNode, 100, 0, (1, 0, 0, 1))
        self.spawnDefenders(base, self.modelNode, 100, 1, (0, 1, 0, 1))

        self.spawnTraveler(base, base_name)

        # print("Space Jam Base placed at " + str(pos))
        self.cNode.setTag("enemy", "base")

        self.orbitTask = SimpleCircleOrbitTask(
            base, self.modelNode, orbit_around, 10, True, OrbitType.XY, True
        )

    def _getLastTravelPos(self):
        return self.travelerPositions[len(self.travelerPositions) - 1]

    def droneWasDestroyed(self, droneCNode: CollisionNode):
        for d in self.defenders:
            if d.cNode.name == droneCNode.name:
                self.dronesDestroyed += 1
                # Removes from list of defenders, but does not yet "destroy"
                self.defenders.remove(d)
                # Let the drone destroy itself (allows managed particle effect)
                d.beginDeath()
                print("Drones Destroyed: " + str(self.dronesDestroyed))
                return

    def spawnDefenders(
        self,
        base: SpaceJamBase,
        parent_node: NodePath,
        count: int,
        pattern: int,
        color_tint: LColor,
    ):
        """Spawns the defenders around the base by way of the given pattern. pattern 0 is a line, pattern 1 is a line of lines. Spawned defenders are added to the base's list."""
        if pattern == 0:
            def_positions = CreateLinePatternPositionsList(
                count, Vec3(0, 0, 0), Vec3(1, 1, -1)
            )
        elif pattern == 1:
            def_positions = CreateLineOfLinePatternsPositionsList(
                int(count * 0.5),
                int(count * 0.5),
                Vec3(0, 0, 0),
                Vec3(-1, 0, 1),
                Vec3(1, -1, -1),
            )
        for pos in def_positions:
            # print("Spawned defender in pattern " + str(pattern) + " at pos " + str(pos))
            spawned = EnemyBaseDrone(
                base,
                parent_node,
                pos,
                color_tint,
                parent_node.name + "def" + str(len(self.defenders)),
            )
            self.defenders.append(spawned)

    def spawnTraveler(
        self,
        base: SpaceJamBase,
        base_name: str,
    ):
        self.travelerPositions: list[Vec3] = []
        self.travelerPositions.append(self.modelNode.getPos())
        self.travelerPositions.append(self._getLastTravelPos() + (10, 10, 10))
        self.travelerPositions.append(self._getLastTravelPos() + (-5, 15, -7.5))
        self.travelerPositions.append(self._getLastTravelPos() + (7.5, -5, 1))
        self.travelerPositions.append(self.modelNode.getPos())
        self.traveler = EnemyTravelDrone(
            base,
            base.render,
            self.modelNode.getPos(),
            (1, 1, 1, 1),
            base_name + "_Traveller",
            self.travelerPositions,
            10,
        )
