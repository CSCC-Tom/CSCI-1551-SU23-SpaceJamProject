from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import CollisionHandlerPusher, CollisionNode, CollisionEntry
from panda3d.core import NodePath
from typing import Callable


class ShipHull(DirectObject):
    """DirectObject that the ship can use to receive events from the ship collider"""

    def __init__(
        self,
        model_node: NodePath,
        collider_node: CollisionNode,
        on_collided_with_object_callback: Callable[[CollisionEntry], None],
    ):
        self.hitpoints = 2
        DirectObject.__init__(self)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(collider_node, model_node)
        collider_node.setTag("player", "ship")
        self.pusher.add_in_pattern("%(player)ft-into-%(neutral)it")
        self.pusher.add_in_pattern("%(player)ft-into-%(enemy)it")
        self.accept(
            "ship-into-neutral",
            on_collided_with_object_callback,
        )
        self.accept(
            "ship-into-base",
            on_collided_with_object_callback,
        )
        self.accept(
            "ship-into-drone",
            on_collided_with_object_callback,
        )
