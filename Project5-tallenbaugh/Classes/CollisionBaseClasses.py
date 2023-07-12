from panda3d.core import (
    PandaNode,
    NodePath,
    CollisionNode,
    CollisionSphere,
    CollisionCapsule,
    CollisionInvSphere,
    Vec3,
)
from Classes import BaseClasses


class GenericCollider(PandaNode):
    """ObjectWithModel with a CollisionNode called cNode"""

    def __init__(self, node_name: str, parent_node: NodePath):
        PandaNode.__init__(self, node_name + "Collider")
        self.cNode = parent_node.attachNewNode(CollisionNode(node_name + "_cNode"))
        self.cNode.show()


class SphereCollider(GenericCollider):
    """CollidableObject with a CollisionSphere solid on the cNode. Default sphere_pos of (0,0,0), default sphere_radius of 1.0"""

    def __init__(
        self,
        parent_node: NodePath,
        node_name: str,
        inverted: bool = False,
        sphere_pos: Vec3 = (0, 0, 0),
        sphere_radius: float = 1.0,
    ):
        GenericCollider.__init__(
            self,
            node_name + "Sphere",
            parent_node,
        )
        shape = (
            CollisionSphere(sphere_pos, sphere_radius)
            if not inverted
            else CollisionInvSphere(sphere_pos, sphere_radius)
        )
        self.cNode.node().addSolid(shape)


class CapsuleCollider(GenericCollider):
    """CollidableObject with a CollisionCapsule solid on the cNode. Default pos_a and _b of (0,0,0) and (0,0,1), default sphere_radius of 1.0"""

    def __init__(
        self,
        parent_node: NodePath,
        node_name: str,
        pos_a: Vec3 = (0, 0, 0),
        pos_b: Vec3 = (0, 0, 1),
        sphere_radius: float = 1.0,
    ):
        super(CapsuleCollider, self).__init__(
            node_name,
            parent_node,
        )
        self.cNode.node().addSolid(CollisionCapsule(pos_a, pos_b, sphere_radius))
