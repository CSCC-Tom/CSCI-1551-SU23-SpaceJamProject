from panda3d.core import Loader, NodePath, CollisionNode
from pandac.PandaModules import Vec3, CollisionHandler
from direct.showbase.DirectObject import DirectObject
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider
from direct.interval.LerpInterval import LerpPosInterval
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
        flight_interrupted_callback: Callable[[CollisionNode], None],
        start_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
        stop_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
    ):
        ProjectileObject.__init__(
            self, loader, model_path, parent_node, node_name, flight_concluded_callback
        )
        self.flightInterruptedCallback = flight_interrupted_callback
        self.startHandlingCollisionsCB = start_handling_collisions_cb
        self.stopHandlingCollisionsCB = stop_handling_collisions_cb

    def flightInterruptedByCollision(self, target_collider: CollisionNode):
        print("PhaserMissile hit a " + target_collider.name)
