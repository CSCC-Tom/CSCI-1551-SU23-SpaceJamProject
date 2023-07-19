from panda3d.core import Loader, PandaNode, NodePath, Texture, Vec3, LColor
from Classes.GameObjects.GameModel import ModelObject
from Classes.GameObjects.GameCollider import SphereCollider


class ModelWithSphereCollider(ModelObject, SphereCollider):
    """Combined base object for all fundamental models with sphere colliders"""

    def __init__(
        self,
        loader: Loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        inverted: bool = False,
        sphere_pos: Vec3 = (0, 0, 0),
        sphere_radius: float = 1.0,
    ):
        ModelObject.__init__(
            self, loader, model_path, parent_node, node_name + "_Model"
        )
        SphereCollider.__init__(
            self,
            self.modelNode,
            node_name + "_SphereCollider",
            inverted,
            sphere_pos,
            sphere_radius,
        )
