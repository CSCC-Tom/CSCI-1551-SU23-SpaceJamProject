from enum import Enum
from panda3d.core import NodePath, Vec3, LColor
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.Enemy.EnemyDrone import EnemyBaseDrone
from Classes.Enemy.EnemyTravelDrone import EnemyTravelDrone


class SpawningPattern(Enum):
    Line = 0
    LineOfLines = 1


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


class DefenderDroneSpawner:
    spawned: list[EnemyBaseDrone]

    def __init__(self, base: SpaceJamBase, enemy_base_node_path: NodePath):
        self.base = base
        self.spawned = []
        self.enemyBaseNode = enemy_base_node_path

    def spawnDefenders(
        self,
        parent_node: NodePath,
        count: int,
        pattern: SpawningPattern,
        color_tint: LColor,
    ):
        """Spawns the defenders around the base by way of the given pattern. pattern 0 is a line, pattern 1 is a line of lines. Spawned defenders are added to the base's list."""
        if pattern == SpawningPattern.Line:
            def_positions = CreateLinePatternPositionsList(
                count, Vec3(0, 0, 0), Vec3(1, 1, -1)
            )
        elif pattern == SpawningPattern.LineOfLines:
            def_positions = CreateLineOfLinePatternsPositionsList(
                int(count * 0.5),
                int(count * 0.5),
                Vec3(0, 0, 0),
                Vec3(-1, 0, 1),
                Vec3(1, -1, -1),
            )
        else:
            def_positions = []

        for pos in def_positions:
            # print("Spawned defender in pattern " + str(pattern) + " at pos " + str(pos))
            spawned = EnemyBaseDrone(
                self.base,
                parent_node,
                pos,
                color_tint,
                parent_node.name + "def" + str(len(self.spawned)),
            )
            self.spawned.append(spawned)

    def _getLastTravelPos(self):
        return self.travelerPositions[len(self.travelerPositions) - 1]

    def spawnTraveler(
        self,
        unique_name: str,
    ):
        self.travelerPositions: list[Vec3] = []
        self.travelerPositions.append(self.enemyBaseNode.getPos())
        self.travelerPositions.append(self._getLastTravelPos() + (10, 10, 10))
        self.travelerPositions.append(self._getLastTravelPos() + (-5, 15, -7.5))
        self.travelerPositions.append(self._getLastTravelPos() + (7.5, -5, 1))
        self.travelerPositions.append(self.enemyBaseNode.getPos())
        self.traveler = EnemyTravelDrone(
            self.base,
            self.base.render,
            self.enemyBaseNode.getPos(),
            (1, 1, 1, 1),
            unique_name + "_Traveller",
            self.travelerPositions,
            10,
        )
