from panda3d.core import Loader, NodePath, CollisionNode
from pandac.PandaModules import Vec3, CollisionHandler
from Classes.GameObjects.ProjectileCollisionHandler import ProjectileCollisionHandler
from typing import Callable


class PhaserMissile(ProjectileCollisionHandler):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        flight_miss_callback: Callable[[ProjectileCollisionHandler], None],
        start_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
        stop_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
    ):
        ProjectileCollisionHandler.__init__(
            self,
            loader,
            "./Assets/Phaser/phaser.egg",
            scene_node,
            "PlayerPhaser",
            self.onProjectileHitNoTargets,
            self.onProjectileHitSomething,
            start_handling_collisions_cb,
            stop_handling_collisions_cb,
        )
        self.flightMissCallback = flight_miss_callback
        self.modelColliderNode.modelNode.setScale(0.1)

    def onProjectileHitNoTargets(self):
        self.flightMissCallback(self)

    def onProjectileHitSomething(self, target_collider: CollisionNode):
        print("PhaserMissile hit a " + target_collider.name)
