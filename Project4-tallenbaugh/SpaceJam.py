import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode
from Classes import SpaceJamClasses, SpaceJamPlayer


def quit():
    """Prepare message if server wants to quit"""
    ## Network contacts will go here
    sys.exit()


class SpaceJam(ShowBase):
    """Base class for the whole Space Jam game, that interfaces with the ShowBase of the Panda3D library."""

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

    def assignCoreKeyBindings(self):
        """Key bindings that involve very core game functions. Currently maps the escape key to the Quit function."""
        self.accept("escape", quit)

    def assignPlayerKeyBindings(self, player: SpaceJamPlayer.SpaceJamPlayerShip):
        """Key bindings between the hardware and the player functions; arrow keys for Heading and Pitch, a/d for Roll, space for Thrust"""
        self.accept("arrow_right", player.headingCWKeyEvent, [1])
        self.accept("arrow_right-up", player.headingCWKeyEvent, [0])
        self.accept("arrow_left", player.headingCCWKeyEvent, [1])
        self.accept("arrow_left-up", player.headingCCWKeyEvent, [0])
        self.accept("arrow_up", player.pitchCWKeyEvent, [1])
        self.accept("arrow_up-up", player.pitchCWKeyEvent, [0])
        self.accept("arrow_down", player.pitchCCWKeyEvent, [1])
        self.accept("arrow_down-up", player.pitchCCWKeyEvent, [0])
        self.accept("a", player.rollCWKeyEvent, [1])
        self.accept("a-up", player.rollCWKeyEvent, [0])
        self.accept("d", player.rollCCWKeyEvent, [1])
        self.accept("d-up", player.rollCCWKeyEvent, [0])
        self.accept("space", player.thrustKeyEvent, [1])
        self.accept("space-up", player.thrustKeyEvent, [0])

    def __init__(self):
        ShowBase.__init__(self)

        self.addTitle("SPACE JAM CLASS EXAMPLE")

        self.assignCoreKeyBindings()

        self.universe = SpaceJamClasses.SpaceJamUniverse(self.loader, self.render)
        self.planets = SpaceJamClasses.SpaceJamSolarSystem(self.loader, self.render)
        self.baseA = SpaceJamClasses.SpaceJamBase(
            self.loader,
            self.render,
            self.planets.mercury.modelNode.getPos() + (8, -8, -8),
        )

        if self.camera == None:
            raise AssertionError("Game did not have a valid camera!")

        self.player = SpaceJamPlayer.SpaceJamPlayerShip(
            self.loader, self.render, self.taskMgr, self.camera
        )
        # Moves the ship somewhere reasonable outside of the Sun
        self.player.shipObj.setPos((50, 60, 30))
        self.assignPlayerKeyBindings(self.player)


app = SpaceJam()
app.run()
