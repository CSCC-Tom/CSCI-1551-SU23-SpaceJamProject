from panda3d.core import PandaNode, NodePath
from direct.particles.ParticleEffect import ParticleEffect
import os


class RetroExplosionEffect(PandaNode):
    """ProjectileObject Missile/Phaser that belongs to the PlayerShip."""

    def __init__(self, objParent: NodePath, sceneNodeParent: NodePath):
        PandaNode.__init__(self, "ParticleEffectRetroExplosion")
        self.explosionEffect = ParticleEffect()
        # Particle effect loading seems to need a different approach from usual asset loading
        # Root folder is "up three levels" from this exact file
        dirname = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        dirname = dirname.replace("C:\\", "/c/")
        dirname = dirname.replace("\\", "/")
        # Particle is at following path from root
        explosion_filename = os.path.join(
            dirname, "Assets", "Particles", "RetroExplosion.ptf"
        )
        self.explosionEffect.loadConfig(explosion_filename)
        self.explosionEffect.start(objParent, sceneNodeParent)
