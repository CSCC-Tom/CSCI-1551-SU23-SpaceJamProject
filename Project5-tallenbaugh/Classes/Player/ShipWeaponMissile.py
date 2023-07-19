from panda3d.core import Loader, NodePath, CollisionNode
from pandac.PandaModules import Vec3, CollisionHandler, CollisionEntry
from Classes.GameObjects.ProjectileCollisionHandler import ProjectileCollisionHandler
from typing import Callable


class PhaserMissile(ProjectileCollisionHandler):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        phaser_miss_callback: Callable[[ProjectileCollisionHandler], None],
        phaser_hit_callback: Callable[
            [ProjectileCollisionHandler, CollisionNode], None
        ],
        start_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
        stop_handling_collisions_cb: Callable[[NodePath], None],
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
        self.phaserMissCallback = phaser_miss_callback
        self.phaserHitCallback = phaser_hit_callback
        self.modelColliderNode.modelNode.setScale(0.1)
        self.accept(
            "PlayerPhaser_SphereColliderSphere_cNode-into-BBQ_SphereColliderSphere_cNode",
            self.onProjectileHitBBQPlanet,
        )
        print(self.modelColliderNode.cNode.name)

    def onProjectileHitBBQPlanet(self, entry: CollisionEntry):
        print(entry)
        self.flightInterruptedByCollision(entry.getIntoNode())

    def onProjectileHitNoTargets(self):
        # print("PhaserMissile hit no targets!")
        self.phaserMissCallback(self)

    def onProjectileHitSomething(self, target_collider: CollisionNode):
        # print("PhaserMissile hit a " + target_collider.name)
        self.phaserHitCallback(self, target_collider)
