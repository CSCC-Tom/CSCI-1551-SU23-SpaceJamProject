from direct.gui.DirectGui import OnscreenText
from pandac.PandaModules import TextNode


class SpaceJamHeadsUpDisplay:
    """Class to handle Onscreen Text stuff so that SpaceJam doesn't have to."""

    def addTitle(self, text: str):
        """Function to put title on the screen."""
        self.title = OnscreenText(
            text=text,
            style=1,
            fg=(1, 1, 1, 1),
            pos=(0.0, -0.95),
            align=TextNode.ACenter,
            scale=0.07,
        )

    def addOnscreenCoreKeyBindings(self):
        """Function to put title on the screen."""
        self.coreKeyInstructions = OnscreenText(
            text="[escape] -> quit",
            style=1,
            fg=(1, 1, 1, 1),
            pos=(-1.3, 0.925),
            align=TextNode.ALeft,
            scale=0.07,
        )

    def addOnscreenPlayerKeyBindings(self):
        """Function to put title on the screen."""

        instructions_text = (
            "[arrow_right] -> turn heading right/clockwise\n"
            + "[arrow_left] -> turn heading left/counter-cw\n"
            + "[arrow_up] -> turn pitch up/cw\n"
            + "[arrow_down] -> turn pitch down/ccw\n"
            + "[a] -> turn roll left/ccw\n"
            + "[d] -> turn roll right/cw\n"
            + "[space] -> thrust / move forward\n"
            + "[f] -> fire missile (if missile is ready)"
        )
        self.playerKeyInstructions = OnscreenText(
            text=instructions_text,
            style=1,
            fg=(1, 1, 1, 1),
            pos=(-1.3, 0.825),
            align=TextNode.ALeft,
            scale=0.07,
        )
