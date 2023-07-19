from panda3d.core import Loader, NodePath
from Classes.Player.ShipWeaponMissile import PhaserMissile
from pandac.PandaModules import Vec3
from direct.interval.LerpInterval import LerpPosInterval
from typing import Callable


class ShipCannon:
    """The 'cannon' of the PlayerShip, that is able to fire PhaserMissiles"""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        ship_position_function: Callable[[], Vec3],
        ship_forward_function: Callable[[], Vec3],
    ):
        # Start the phaser in "active" so we can call reload to prep it.
        self.activeMissile = PhaserMissile(loader, scene_node)
        self.reloadedMissile = None
        self.getFirePos = ship_position_function
        self.getFireDir = ship_forward_function
        self.reload()

    def fireMissileIfReady(self):
        """If the missile is in the reloadedMissile slot, then we kick it off as an active missile"""
        if self.reloadedMissile == None:
            # Don't have a reloaded missile to fire. Something else should call reload() first.
            return

        # Ready - Move the missile in place to get ready to follow its Interval
        self.activeMissile = self.reloadedMissile
        self.reloadedMissile = None
        missileStartPos = self.getFirePos() + (self.getFireDir() * 5)
        self.activeMissile.modelNode.setPos(missileStartPos)
        # Aim - Set the target pos and build the Interval
        missileTargetPos = missileStartPos + (self.getFireDir() * 500)
        self.activeMissile.fireInterval = LerpPosInterval(
            self.activeMissile.modelNode,
            2,
            missileTargetPos,
            missileStartPos,
            None,
            "noBlend",
            1,
            1,
            "missileFireInterval",
        )
        # Fire!
        self.activeMissile.fireInterval.start()

    def reload(self):
        """Function that takes the active missile and makes it readied again."""
        if self.reloadedMissile != None:
            # There is already a reloaded missile. Something else should call fireMissileIfReady() first.
            return

        self.reloadedMissile = self.activeMissile
        # Not 100% that this will work, but haven't build reloading logic yet.
        self.reloadedMissile.fireInterval = {}
        # Stick the "reloaded" missile somewhere far away so we don't see it.
        self.reloadedMissile.modelNode.setPos((9000, 9000, 9000))
        self.activeMissile = None
