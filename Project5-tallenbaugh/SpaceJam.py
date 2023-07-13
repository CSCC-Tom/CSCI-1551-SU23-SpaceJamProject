import sys
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode, CollisionHandlerPusher, CollisionTraverser
from Classes import SpaceJamClasses, SpaceJamPlayer
from Classes.Player import ShipMovement


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

    def addOnscreenDebugKeyBindings(self):
        """Function to put title on the screen."""
        self.debugKeyInstructions = OnscreenText(
            text="[s] -> superspeed(False, 1)",
            style=1,
            fg=(1, 1, 1, 1),
            pos=(1.3, 0.925),
            align=TextNode.ARight,
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

    def toggleDebugSuperSpeed(self):
        """Function to make the player go very very fast to test the edge of the universe, or to return speed to normal."""

        self.superSpeedActive = not self.superSpeedActive
        self.player.movement.thrustRate = (
            ShipMovement.DEFAULT_PLAYER_THRUST_RATE
            if not self.superSpeedActive
            else 9000
        )
        self.debugKeyInstructions.text = (
            "[s] -> superspeed("
            + str(self.superSpeedActive)
            + ", "
            + str(self.player.movement.thrustRate)
            + ")"
        )

    def assignDebugKeyBindings(self):
        """Key bindings that involve the developer debugging the game. Should not be used in a released version. Currently maps the s key to the Super Speed function."""

        self.accept("s", self.toggleDebugSuperSpeed)
        self.addOnscreenDebugKeyBindings()

    def assignCoreKeyBindings(self):
        """Key bindings that involve very core game functions. Currently maps the escape key to the Quit function."""
        self.accept("escape", quit)
        self.addOnscreenCoreKeyBindings()

    def preparePlayerTraverser(self):
        if not isinstance(self.player, SpaceJamPlayer.PlayerController):
            raise AssertionError(
                "Space Jam called preparePlayerTraverser() but did not have a self.player!"
            )
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.player.cNode, self.player.modelNode)
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.cTrav.addCollider(self.player.cNode, self.pusher)
        self.cTrav.showCollisions(self.render)

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

        self.player = SpaceJamPlayer.PlayerController(
            self.loader, self.render, self.taskMgr, self.camera, self.accept
        )

        # Moves the ship somewhere reasonable outside of the Sun
        self.player.modelNode.setPos((50, 60, 30))
        self.addOnscreenPlayerKeyBindings()
        self.preparePlayerTraverser()

        # Debug tools
        self.superSpeedActive = False
        self.assignDebugKeyBindings()


app = SpaceJam()
app.run()
