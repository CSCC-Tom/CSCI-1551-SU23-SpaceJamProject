from panda3d.core import Loader, NodePath
from pandac.PandaModules import CollisionHandler, CollisionHandlerEvent
from typing import Callable
from Classes.GameObjects.Projectile import ProjectileObject


class ProjectileCollisionHandler(ProjectileObject):
    def __init__(
        self,
        loader: Loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        flight_concluded_callback: Callable[[], None],
        start_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
        stop_handling_collisions_cb: Callable[[NodePath], None],
        collision_in_patterns: list[str],
    ):
        ProjectileObject.__init__(
            self, loader, model_path, parent_node, node_name, flight_concluded_callback
        )
        self.collisionHandler = CollisionHandlerEvent()
        for in_pattern in collision_in_patterns:
            self.collisionHandler.add_in_pattern(in_pattern)
        self.startHandlingCollisionsCB = start_handling_collisions_cb
        self.stopHandlingCollisionsCB = stop_handling_collisions_cb

    def flightInterruptedByCollision(self):
        self.concludeFlight(True)

    def commenceFlight(self):
        ProjectileObject.commenceFlight(self)
        self.startHandlingCollisionsCB(
            self.modelColliderNode.cNode, self.collisionHandler
        )

    def concludeFlight(self, interrupted: bool):
        ProjectileObject.concludeFlight(self, interrupted)
        self.stopHandlingCollisionsCB(self.modelColliderNode.cNode)
