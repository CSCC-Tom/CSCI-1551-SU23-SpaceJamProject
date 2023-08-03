from panda3d.core import NodePath, Vec3, LColor
from Classes.GameObjects.DestructibleShip import (
    DestructibleShip,
)
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class EnemyBaseDrone(DestructibleShip):
    """Object spawned and managed by a Base that has a model and collider"""

    def __init__(
        self,
        base: SpaceJamBase,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
    ):
        DestructibleShip.__init__(
            self,
            base,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            pos,
            col_tint,
            node_name + "Model",
        )

        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
        # print("Spawned Defender(" + node_name + ")")
        self.cNode.setTag("enemy", "drone")
