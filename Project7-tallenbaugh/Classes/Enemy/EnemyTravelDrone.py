from panda3d.core import NodePath, Vec3, LColor
from Classes.Enemy.EnemyDrone import (
    EnemyBaseDrone,
)
from Classes.GameObjects.ParticleExplosionRetro import RetroExplosionEffect
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.Gameplay.TravelerLogic import SimplePointBasedTravelTask
import threading


class EnemyTravelDrone(EnemyBaseDrone):
    """Object spawned and managed by a Base that has a model and collider"""

    def __init__(
        self,
        base: SpaceJamBase,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
        travel_positions: list[Vec3],
        travel_duration: float,
    ):
        EnemyBaseDrone.__init__(
            self,
            base,
            parent_node,
            pos,
            col_tint,
            node_name,
        )
        self.travelLogic = SimplePointBasedTravelTask(
            node_name + "_Travel", self.modelNode, travel_positions, travel_duration
        )
