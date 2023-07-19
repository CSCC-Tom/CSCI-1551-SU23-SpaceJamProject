from panda3d.core import Loader, NodePath, Vec3, LColor
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
)


class EnemyBaseDrone(ModelWithSphereCollider):
    """Object spawned and managed by a Base that has a model and collider"""

    def __init__(
        self,
        loader: Loader,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
    ):
        ModelWithSphereCollider.__init__(
            self,
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            node_name + "Model",
        )

        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
        # print("Spawned Defender(" + node_name + ")")
