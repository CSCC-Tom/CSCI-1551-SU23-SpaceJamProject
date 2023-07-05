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
        self.accept("arrow_right", self.player.headingCWKeyEvent, [1])
        self.accept("arrow_right-up", self.player.headingCWKeyEvent, [0])
        self.accept("arrow_left", self.player.headingCCWKeyEvent, [1])
        self.accept("arrow_left-up", self.player.headingCCWKeyEvent, [0])
        self.accept("arrow_up", self.player.pitchCWKeyEvent, [1])
        self.accept("arrow_up-up", self.player.pitchCWKeyEvent, [0])
        self.accept("arrow_down", self.player.pitchCCWKeyEvent, [1])
        self.accept("arrow_down-up", self.player.pitchCCWKeyEvent, [0])
        self.accept("a", self.player.rollCWKeyEvent, [1])
        self.accept("a-up", self.player.rollCWKeyEvent, [0])
        self.accept("d", self.player.rollCCWKeyEvent, [1])
        self.accept("d-up", self.player.rollCCWKeyEvent, [0])
        self.accept("space", self.player.thrustKeyEvent, [1])
        self.accept("space-up", self.player.thrustKeyEvent, [0])

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
