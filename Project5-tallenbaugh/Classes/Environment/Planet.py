from panda3d.core import Loader, NodePath, Vec3
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
)


class SpaceJamPlanet(ModelWithSphereCollider):
    """ModelWithSphereCollider representing a Planet"""

    def __init__(
        self,
        loader: Loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        position: Vec3,
        scale: float,
    ):
        ModelWithSphereCollider.__init__(
            self, loader, model_path, parent_node, node_name
        )

        # Note position of 0 above to make sure the collider matches visual position, and then both are moved by moving the parent modelNode.
        self.modelNode.setPos(position)
        # Note scale of 1 above to make sure the collider matches visual size, and THEN we scale both up together by scaling the parent modelNode.
        self.modelNode.setScale(scale)
