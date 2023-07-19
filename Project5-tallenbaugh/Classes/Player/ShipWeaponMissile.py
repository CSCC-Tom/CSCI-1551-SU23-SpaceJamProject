from panda3d.core import Loader, NodePath
from Classes.GameObjects.Projectile import ProjectileObject


class PhaserMissile(ProjectileObject):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
    ):
        ProjectileObject.__init__(
            self, loader, "./Assets/Phaser/phaser.egg", scene_node, "PlayerPhaser"
        )
        self.modelColliderNode.modelNode.setScale(0.1)
