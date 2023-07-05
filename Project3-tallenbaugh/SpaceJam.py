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
        """Key bindings that involve very core functions"""
        self.accept("escape", quit)

    def assignPlayerKeyBindings(self):
        """Key bindings that are specific to the Player"""
        self.accept("arrow_right", self.player.headingClockwiseKeyEvent, [1])
        self.accept("arrow_right-up", self.player.headingClockwiseKeyEvent, [0])

    def __init__(self):
        ShowBase.__init__(self)

        self.addTitle("SPACE JAM CLASS EXAMPLE")

        self.assignCoreKeyBindings()

        self.universe = SpaceJamClasses.SpaceJamUniverse(self.loader, self.render)
        self.planets = SpaceJamClasses.SpaceJamPlanets(self.loader, self.render)
        self.baseA = SpaceJamClasses.SpaceJamBase(
            self.loader, self.render, self.planets.mercury.getPos() + (8, -8, -8)
        )

        if self.camera == None:
            raise AssertionError("Game did not have a valid camera!")

        self.player = SpaceJamPlayer.SpaceJamPlayerShip(
            self.loader, self.render, self.taskMgr, self.camera
        )
        self.assignPlayerKeyBindings()


app = SpaceJam()
app.run()
