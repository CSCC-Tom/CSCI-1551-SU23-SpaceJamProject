from panda3d.core import NodePath, Vec3, LColor
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
)
from Classes.GameObjects.ParticleExplosionRetro import RetroExplosionEffect
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
import threading


class EnemyBaseDrone(ModelWithSphereCollider):
    """Object spawned and managed by a Base that has a model and collider"""

    def __init__(
        self,
        base: SpaceJamBase,
        parent_node: NodePath,
        pos: Vec3,
        col_tint: LColor,
        node_name: str,
    ):
        ModelWithSphereCollider.__init__(
            self,
            base,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            node_name + "Model",
        )

        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
        # print("Spawned Defender(" + node_name + ")")
        self.cNode.setTag("enemy", "drone")

    def beginDeath(self):
        # Start our explosion effect
        self.deathExplosion = RetroExplosionEffect(
            self.modelNode,
            self.modelNode.parent.parent
            # modelNode.parent should be the enemy base
            # parent of that should be the spacejam render
        )
        self.cNode.removeNode()
        self.deathTimer = threading.Timer(1, self.midDeath)
        self.deathTimer.start()

    def midDeath(self):
        self.modelNode.hide()
        self.deathTimer = threading.Timer(1, self.concludeDeath)
        self.deathTimer.start()

    def concludeDeath(self):
        # modelNode is the heart nodepath of a ModelWithCollider object
        # When "removeNode" is called, Panda will no longer have any references to this drone
        # and it will be removed from memory and will disappear.
        self.deathExplosion.explosionEffect.cleanup()
        self.modelNode.removeNode()
