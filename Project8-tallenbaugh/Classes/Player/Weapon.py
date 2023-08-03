from Classes.Player.WeaponProjectile import PhaserMissile
from Classes.Player.GyroSensors import ShipGyroscope
from pandac.PandaModules import CollisionNode
from typing import Callable
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class ShipCannon:
    """The 'cannon' of the PlayerShip, that is able to fire PhaserMissiles"""

    disabled = False

    def __init__(
        self,
        base: SpaceJamBase,
        ship_gyro: ShipGyroscope,
        missile_hit_enemy_drone_cb: Callable[[PhaserMissile, CollisionNode], None],
        missile_hit_enemy_base_cb: Callable[[PhaserMissile, CollisionNode], None],
    ):
        # Start the phaser in "active" so we can call reload to prep it.
        self.activeMissile = PhaserMissile(
            base,
            self.onMissileHitNoTargets,
            self.onMissileHitSomeTarget,
        )
        self.reloadedMissile = None
        self.getFirePos = ship_gyro.getShipPos
        self.getFireDir = ship_gyro.getShipForward
        self.onHitDroneCB = missile_hit_enemy_drone_cb
        self.onHitBaseCB = missile_hit_enemy_base_cb

        self.reload()

    def disable(self):
        self.disabled = True

    def fireMissileIfReady(self):
        """If the missile is in the reloadedMissile slot, then we kick it off as an active missile"""
        if self.reloadedMissile == None:
            # Don't have a reloaded missile to fire. Something else should call reload() first.
            return
        if self.disabled == True:
            return

        # Ready - Move the missile in place to get ready to follow its Interval
        self.activeMissile = self.reloadedMissile
        self.reloadedMissile = None
        missileStartPos = self.getFirePos() + (self.getFireDir() * 5)
        # Aim - Set the target pos and build the Interval
        self.activeMissile.prepareFlight(missileStartPos, self.getFireDir(), 1000)
        # Fire!
        self.activeMissile.commenceFlight()

    def reload(self):
        """Function that takes the active missile and makes it readied again."""
        if self.reloadedMissile != None:
            # There is already a reloaded missile. Something else should call fireMissileIfReady() first.
            return

        self.reloadedMissile = self.activeMissile
        self.activeMissile = None

    def onMissileHitNoTargets(self, missile: PhaserMissile):
        if self.activeMissile is not missile:
            raise AssertionError(
                "ShipCannon.onMissileHitNoTargets called, but the missile was not the active expected missile..."
            )

        self.reload()

    def onMissileHitSomeTarget(self, missile: PhaserMissile, target: CollisionNode):
        self.reload()
        if target.hasTag("enemy"):
            if target.getTag("enemy") == "drone":
                self.onHitDroneCB(missile, target)
            if target.getTag("enemy") == "base":
                self.onHitBaseCB(missile, target)
