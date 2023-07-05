from panda3d.core import NodePath, CollisionNode, CollisionSphere, Vec3
from Classes import BaseClasses


class CollidableObject(BaseClasses.ObjectWithModel, object):
    """ObjectWithModel with a CollisionNode called cNode"""

    def __init__(self, loader, model_path: str, parent_node: NodePath, node_name: str):
        super(CollidableObject, self).__init__(
            loader, model_path, parent_node, node_name
        )
        self.cNode = self.modelNode.attachNewNode(CollisionNode(node_name + "_cNode"))


class SphereCollidableObject(CollidableObject, object):
    """CollidableObject with a CollisionSphere solid on the cNode. Default sphere_pos of (0,0,0), default sphere_radius of 1.0"""

    def __init__(
        self,
        loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        sphere_pos: Vec3 = (0, 0, 0),
        sphere_radius: float = 1.0,
    ):
        super(SphereCollidableObject, self).__init__(
            loader, model_path, parent_node, node_name
        )
        self.cNode.node().addSolid(
            CollisionSphere(sphere_pos[0], sphere_pos[1], sphere_pos[2], sphere_radius)
        )
        # Uncomment this next line to make the collider visible, for testing/debugging only.
        # self.cNode.show()
