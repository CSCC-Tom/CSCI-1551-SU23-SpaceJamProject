from enum import Enum
from Classes.Player.Movement import ShipThrusters
from Classes.Player.Weapon import ShipCannon

from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class KeyState(Enum):
    KeyUp = 0
    KeyDown = 1


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
        base.accept("arrow_right", self.headingCWKeyEvent, [KeyState.KeyDown])
        base.accept("arrow_right-up", self.headingCWKeyEvent, [KeyState.KeyUp])
        base.accept("arrow_left", self.headingCCWKeyEvent, [KeyState.KeyDown])
        base.accept("arrow_left-up", self.headingCCWKeyEvent, [KeyState.KeyUp])
        base.accept("arrow_up", self.pitchCWKeyEvent, [KeyState.KeyDown])
        base.accept("arrow_up-up", self.pitchCWKeyEvent, [KeyState.KeyUp])
        base.accept("arrow_down", self.pitchCCWKeyEvent, [KeyState.KeyDown])
        base.accept("arrow_down-up", self.pitchCCWKeyEvent, [KeyState.KeyUp])
        base.accept("a", self.rollCCWKeyEvent, [KeyState.KeyDown])
        base.accept("a-up", self.rollCCWKeyEvent, [KeyState.KeyUp])
        base.accept("d", self.rollCWKeyEvent, [KeyState.KeyDown])
        base.accept("d-up", self.rollCWKeyEvent, [KeyState.KeyUp])
        base.accept("space", self.thrustKeyEvent, [KeyState.KeyDown])
        base.accept("space-up", self.thrustKeyEvent, [KeyState.KeyUp])
        # Fire!
        base.accept("f", self.cannon.fireMissileIfReady)

    # KEY EVENT INPUT HELPERS
    # used to turn one-time "keyup" and "keydown" events into a continuous task called during every "frame" of the game where the button is held down.
    def headingCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipHeadingCW, "rotateShipHeadingCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCW")

    def headingCCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipHeadingCCW, "rotateShipHeadingCCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCCW")

    def pitchCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipPitchCW, "rotateShipPitchCW")
        else:
            self.taskMgr.remove("rotateShipPitchCW")

    def pitchCCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipPitchCCW, "rotateShipPitchCCW")
        else:
            self.taskMgr.remove("rotateShipPitchCCW")

    def rollCCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipRollCCW, "rotateShipRollCCW")
        else:
            self.taskMgr.remove("rotateShipRollCCW")

    def rollCWKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.rotateShipRollCW, "rotateShipRollCW")
        else:
            self.taskMgr.remove("rotateShipRollCW")

    def thrustKeyEvent(self, key_state: KeyState):
        if key_state == KeyState.KeyDown:
            self.taskMgr.add(self.movement.addShipThrust, "addShipThrust")
        else:
            self.taskMgr.remove("addShipThrust")
