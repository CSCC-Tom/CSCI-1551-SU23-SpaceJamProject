from panda3d.core import Loader, NodePath
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider
from direct.interval.LerpInterval import LerpPosInterval


class PhaserMissile(ModelWithSphereCollider):
    """Missile/Phaser that belongs to the PlayerShip."""

    fireInterval: LerpPosInterval = {}

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
    ):
        ModelWithSphereCollider.__init__(
            self, loader, "./Assets/Phaser/phaser.egg", scene_node, "PlayerPhaser"
        )
        self.modelNode.setScale(0.1)
