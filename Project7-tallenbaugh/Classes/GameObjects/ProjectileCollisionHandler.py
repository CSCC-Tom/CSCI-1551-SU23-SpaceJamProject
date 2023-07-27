from pandac.PandaModules import CollisionHandlerEvent
from typing import Callable
from Classes.GameObjects.Projectile import ProjectileObject
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class ProjectileCollisionHandler(ProjectileObject):
    def __init__(
        self,
        base: SpaceJamBase,
        model_path: str,
        node_name: str,
        flight_concluded_callback: Callable[[], None],
        collision_in_patterns: list[str],
    ):
        ProjectileObject.__init__(
            self,
            base,
            model_path,
            node_name,
            flight_concluded_callback,
        )
        self.collisionHandler = CollisionHandlerEvent()
        for in_pattern in collision_in_patterns:
            self.collisionHandler.add_in_pattern(in_pattern)
        self.startHandlingCollisionsCB = (
            base.sjTraverser.startTrackingCollisionsForHandler
        )
        self.stopHandlingCollisionsCB = (
            base.sjTraverser.stopTrackingCollisionsForHandler
        )

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
