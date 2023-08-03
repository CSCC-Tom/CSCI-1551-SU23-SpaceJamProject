from panda3d.core import CollisionNode
from pandac.PandaModules import CollisionEntry
from Classes.GameObjects.ProjectileCollisionHandler import ProjectileCollisionHandler
from typing import Callable
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class PhaserMissile(ProjectileCollisionHandler):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(
        self,
        base: SpaceJamBase,
        phaser_miss_callback: Callable[[ProjectileCollisionHandler], None],
        phaser_hit_callback: Callable[
            [ProjectileCollisionHandler, CollisionNode], None
        ],
    ):
        ProjectileCollisionHandler.__init__(
            self,
            base,
            "./Assets/Phaser/phaser.egg",
            "PlayerPhaser",
            self.onProjectileHitNoTargets,
            ["%(player)ft-into-%(neutral)it", "%(player)ft-into-%(enemy)it"],
        )
        self.sceneNodeParent = base.render
        self.modelColliderNode.cNode.setTag("player", "missile")
        self.phaserMissCallback = phaser_miss_callback
        self.phaserHitCallback = phaser_hit_callback
        self.modelColliderNode.modelNode.setScale(0.1)
        self.accept(
            "missile-into-neutral",
            self.onProjectileHitEnvironment,
        )
        self.accept(
            "missile-into-base",
            self.onProjectileHitEnemyBase,
        )
        self.accept(
            "missile-into-drone",
            self.onProjectileHitEnemyDrone,
        )

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
