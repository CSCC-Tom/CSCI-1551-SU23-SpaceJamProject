from panda3d.core import Loader, NodePath
from Classes import BaseClasses, CollisionBaseClasses
from direct.task import Task
from pandac.PandaModules import Vec3
from direct.task.Task import TaskManager
from direct.interval.LerpInterval import LerpPosInterval


class PlayerPhaser(BaseClasses.ModelObject, CollisionBaseClasses.SphereCollider):
    """Missile/Phaser that belongs to the PlayerShip."""

    fireInterval: LerpPosInterval = {}

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
    ):
        BaseClasses.ModelObject.__init__(
            self, loader, "./Assets/Phaser/phaser.egg", scene_node, "PlayerPhaser"
        )
        CollisionBaseClasses.SphereCollider.__init__(
            self, self.modelNode, "PlayerPhaser"
        )
        self.modelNode.setScale(0.1)
