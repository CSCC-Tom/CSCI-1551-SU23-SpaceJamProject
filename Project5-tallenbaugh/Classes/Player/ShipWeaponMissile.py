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
            start_handling_collisions_cb,
            stop_handling_collisions_cb,
            ["%(player)ft-into-%(neutral)it", "%(player)ft-into-%(enemy)it"],
        )
        self.modelColliderNode.cNode.setTag("player", "player")
        self.phaserMissCallback = phaser_miss_callback
        self.phaserHitCallback = phaser_hit_callback
        self.modelColliderNode.modelNode.setScale(0.1)
        self.accept(
            "player-into-neutral",
            self.onProjectileHitEnvironment,
        )
        self.accept(
            "player-into-base",
            self.onProjectileHitEnemyBase,
        )
        self.accept(
            "player-into-drone",
            self.onProjectileHitEnemyDrone,
        )
        print(self.modelColliderNode.cNode.name)

    def onProjectileHitNoTargets(self):
        # print("PhaserMissile hit no targets!")
        self.phaserMissCallback(self)

    def onProjectileHitEnvironment(self, entry: CollisionEntry):
        print("ENVIRONMENT: " + str(entry))
        self.flightInterruptedByCollision()
        self.phaserMissCallback(self)

    def onProjectileHitEnemyBase(self, entry: CollisionEntry):
        print("ENEMY BASE: " + str(entry))
        self.flightInterruptedByCollision()
        self.phaserHitCallback(self, entry.getIntoNode())

    def onProjectileHitEnemyDrone(self, entry: CollisionEntry):
        print("ENEMY DRONE: " + str(entry))
        self.flightInterruptedByCollision()
        self.phaserHitCallback(self, entry.getIntoNode())