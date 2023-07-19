from typing import Callable
from direct.gui.OnscreenText import TextNode, OnscreenText
from Classes.Player import ShipMovement as SM


class DebugActions:
    """Class responsible for logic that is only meant for helping build/test the game, not for the game itself."""

    def __init__(
        self,
        input_accept: Callable[[str, Callable, []], None],
        player_movement: SM.ShipMovement,
    ):
        self.superSpeedActive = False
        self.playerMovement = player_movement
        # add Onscreen Debug Key Bindings
        self.debugOST = OnscreenText(
            text="[s] -> superspeed(False, 1)",
            style=1,
            fg=(1, 1, 1, 1),
            pos=(1.3, 0.925),
            align=TextNode.ARight,
            scale=0.07,
        )
        # assign Debug Key Bindings
        # Key bindings that involve the developer debugging the game. Should not be used in a released version.
        # Currently maps the s key to the Super Speed function.
        input_accept("s", self.toggleDebugSuperSpeed)

    def toggleDebugSuperSpeed(self):
        """Function to make the player go very very fast to test the edge of the universe, or to return speed to normal."""

        self.superSpeedActive = not self.superSpeedActive
        self.playerMovement.thrustRate = (
            SM.DEFAULT_PLAYER_THRUST_RATE if not self.superSpeedActive else 9000
        )
        self.debugOST.text = (
            "[s] -> superspeed("
            + str(self.superSpeedActive)
            + ", "
            + str(self.playerMovement.thrustRate)
            + ")"
        )
