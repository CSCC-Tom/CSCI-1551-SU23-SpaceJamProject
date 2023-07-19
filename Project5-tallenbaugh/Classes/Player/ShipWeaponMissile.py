from panda3d.core import Loader, NodePath
from Classes.GameObjects.Projectile import ProjectileObject
from typing import Callable


class PhaserMissile(ProjectileObject):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        flight_miss_callback: Callable[[ProjectileObject], None],
    ):
        ProjectileObject.__init__(
            self,
            loader,
            "./Assets/Phaser/phaser.egg",
            scene_node,
            "PlayerPhaser",
            self.onProjectileHitNoTargets,
        )
        self.flightMissCallback = flight_miss_callback
        self.modelColliderNode.modelNode.setScale(0.1)

    def onProjectileHitNoTargets(self):
        self.flightMissCallback(self)
