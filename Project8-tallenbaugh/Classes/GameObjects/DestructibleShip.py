from panda3d.core import NodePath, Vec3, LColor
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
)
from Classes.GameObjects.ParticleExplosionRetro import RetroExplosionEffect
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
import threading


class DestructibleShip(ModelWithSphereCollider):
    """ModelWithSphereCollider object that is able to 'explode' when 'dead'."""

    timePerDeathStep = 1.0

    def __init__(
        self,
        base: SpaceJamBase,
        asset_path: str,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
    ):
        ModelWithSphereCollider.__init__(
            self,
            base,
            asset_path,
            parent_node,
            node_name + "Model",
        )
        self.clock = base.clock
        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
        # print("Spawned Defender(" + node_name + ")")
        self.cNode.setTag("enemy", "drone")

    def beginDeath(self):
        self.timeOfDeath = self.clock.getRealTime()
        # Start our explosion effect
        self.deathExplosion = RetroExplosionEffect(
            self.modelNode,
            self.modelNode.parent.parent
            # modelNode.parent should be the enemy base
            # parent of that should be the spacejam render
        )
        self.cNode.removeNode()
        self.deathTimer = threading.Timer(self.timePerDeathStep, self.midDeath)
        self.deathTimer.start()

    def midDeath(self):
        self.modelNode.hide()
        self.deathTimer = threading.Timer(self.timePerDeathStep, self.concludeDeath)
        self.deathTimer.start()

    def concludeDeath(self):
        # modelNode is the heart nodepath of a ModelWithCollider object
        # When "removeNode" is called, Panda will no longer have any references to this drone
        # and it will be removed from memory and will disappear.
        self.deathExplosion.explosionEffect.cleanup()
        self.modelNode.removeNode()
