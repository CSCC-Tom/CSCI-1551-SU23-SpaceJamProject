from panda3d.core import Loader, NodePath
from Classes.Player.ShipWeaponMissile import PhaserMissile
from pandac.PandaModules import Vec3
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
        self.reload(True)

    def fireMissileIfReady(self):
        """If the missile is in the reloadedMissile slot, then we kick it off as an active missile"""
        if self.reloadedMissile == None:
            # Don't have a reloaded missile to fire. Something else should call reload() first.
            return

        # Ready - Move the missile in place to get ready to follow its Interval
        self.activeMissile = self.reloadedMissile
        self.reloadedMissile = None
        missileStartPos = self.getFirePos() + (self.getFireDir() * 5)
        # Aim - Set the target pos and build the Interval
        self.activeMissile.prepareFlight(missileStartPos, self.getFireDir(), 500)
        # Fire!
        self.activeMissile.commenceFlight()

    def reload(self, init=False):
        """Function that takes the active missile and makes it readied again."""
        if self.reloadedMissile != None:
            # There is already a reloaded missile. Something else should call fireMissileIfReady() first.
            return

        self.reloadedMissile = self.activeMissile
        if init == False:
            self.activeMissile.concludeFlight()
        self.activeMissile = None
