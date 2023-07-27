from Classes.Player.Movement import ShipThrusters
from Classes.Player.Weapon import ShipCannon

from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class PlayerActionHandler:
    """Class responsible for handling raw input intended for player actions."""

    def __init__(
        self,
        base: SpaceJamBase,
        player_movement: ShipThrusters,
        ship_cannon: ShipCannon,
    ):
        self.taskMgr = base.taskMgr
        self.movement = player_movement
        self.cannon = ship_cannon
        # Key bindings between the hardware and the player functions; arrow keys for Heading and Pitch, a/d for Roll, space for Thrust
        base.accept("arrow_right", self.headingCWKeyEvent, [1])
        base.accept("arrow_right-up", self.headingCWKeyEvent, [0])
        base.accept("arrow_left", self.headingCCWKeyEvent, [1])
        base.accept("arrow_left-up", self.headingCCWKeyEvent, [0])
        base.accept("arrow_up", self.pitchCWKeyEvent, [1])
        base.accept("arrow_up-up", self.pitchCWKeyEvent, [0])
        base.accept("arrow_down", self.pitchCCWKeyEvent, [1])
        base.accept("arrow_down-up", self.pitchCCWKeyEvent, [0])
        base.accept("a", self.rollCCWKeyEvent, [1])
        base.accept("a-up", self.rollCCWKeyEvent, [0])
        base.accept("d", self.rollCWKeyEvent, [1])
        base.accept("d-up", self.rollCWKeyEvent, [0])
        base.accept("space", self.thrustKeyEvent, [1])
        base.accept("space-up", self.thrustKeyEvent, [0])
        # Fire!
        base.accept("f", self.cannon.fireMissileIfReady)

    # KEY EVENT INPUT HELPERS
    # used to turn one-time "keyup" and "keydown" events into a continuous task called during every "frame" of the game where the button is held down.
    def headingCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipHeadingCW, "rotateShipHeadingCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCW")

    def headingCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipHeadingCCW, "rotateShipHeadingCCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCCW")

    def pitchCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipPitchCW, "rotateShipPitchCW")
        else:
            self.taskMgr.remove("rotateShipPitchCW")

    def pitchCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipPitchCCW, "rotateShipPitchCCW")
        else:
            self.taskMgr.remove("rotateShipPitchCCW")

    def rollCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipRollCCW, "rotateShipRollCCW")
        else:
            self.taskMgr.remove("rotateShipRollCCW")

    def rollCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.rotateShipRollCW, "rotateShipRollCW")
        else:
            self.taskMgr.remove("rotateShipRollCW")

    def thrustKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.movement.addShipThrust, "addShipThrust")
        else:
            self.taskMgr.remove("addShipThrust")
