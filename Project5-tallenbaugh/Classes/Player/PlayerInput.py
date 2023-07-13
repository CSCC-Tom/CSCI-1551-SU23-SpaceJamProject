from typing import Callable
from Classes.Player.ShipMovement import ShipMovement
from Classes.Player.ShipWeapon import ShipCannon
from direct.task.Task import TaskManager


class PlayerInput:
    """Class responsible for handling raw input intended for player actions."""

    def __init__(
        self,
        # Callable is a 'helper type' you can import.
        # Here it's saying that "inputAccept" is a function that takes a string, another function, and some list, and returns None.
        # That is actually more accurate than what SpaceJam.accept is designed to take, so the typing is able to guide us.
        input_accept: Callable[[str, Callable, []], None],
        player_movement: ShipMovement,
        ship_cannon: ShipCannon,
        task_manager: TaskManager,
    ):
        self.taskMgr = task_manager
        self.movement = player_movement
        self.cannon = ship_cannon
        # Key bindings between the hardware and the player functions; arrow keys for Heading and Pitch, a/d for Roll, space for Thrust
        input_accept("arrow_right", self.headingCWKeyEvent, [1])
        input_accept("arrow_right-up", self.headingCWKeyEvent, [0])
        input_accept("arrow_left", self.headingCCWKeyEvent, [1])
        input_accept("arrow_left-up", self.headingCCWKeyEvent, [0])
        input_accept("arrow_up", self.pitchCWKeyEvent, [1])
        input_accept("arrow_up-up", self.pitchCWKeyEvent, [0])
        input_accept("arrow_down", self.pitchCCWKeyEvent, [1])
        input_accept("arrow_down-up", self.pitchCCWKeyEvent, [0])
        input_accept("a", self.rollCCWKeyEvent, [1])
        input_accept("a-up", self.rollCCWKeyEvent, [0])
        input_accept("d", self.rollCWKeyEvent, [1])
        input_accept("d-up", self.rollCWKeyEvent, [0])
        input_accept("space", self.thrustKeyEvent, [1])
        input_accept("space-up", self.thrustKeyEvent, [0])
        # Fire!
        input_accept("f", self.cannon.fireMissileIfReady)

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
