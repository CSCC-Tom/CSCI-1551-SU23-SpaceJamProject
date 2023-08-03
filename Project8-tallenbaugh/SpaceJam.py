import sys
from enum import Enum
from direct.showbase.ShowBase import ShowBase
from Classes.HUD.HeadsUpDisplay import SpaceJamHeadsUpDisplay
from Classes.SpaceJamPlayer import PlayerController
from Classes.Gameplay.Traversal import SpaceJamTraverser
from Classes.Environment.Universe import SpaceJamUniverse
from Classes.Environment.SolarSystem import SpaceJamSolarSystem
from Classes.Enemy.EnemyBase import SpaceJamEnemyBase
from Classes.Debug.SpaceJamDebug import DebugActions
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


def quit():
    """Prepare message if server wants to quit"""
    ## Network contacts will go here
    sys.exit()


class GameState(Enum):
    Active = 0
    Victory = 1
    Defeat = 2


class SpaceJam(ShowBase):
    """Base class for the whole Space Jam game, that interfaces with the ShowBase of the Panda3D library."""

    def assignCoreKeyBindings(self):
        """Key bindings that involve very core game functions. Currently maps the escape key to the Quit function."""
        self.accept("escape", quit)
        self.hud.addOnscreenCoreKeyBindings()

    def __init__(self):
        ShowBase.__init__(self)

        self.gameState = GameState.Active

        # Onscreen text
        self.hud = SpaceJamHeadsUpDisplay()

        self.hud.addOrUpdateTitle("SPACE JAM : Destroy 30 green/red Drones!")

        self.assignCoreKeyBindings()
        self.enableParticles()  # <-- Particles won't work without this

        # Collisions and traversal
        # Saving this to its own special variable because it is our wrapper around the true traverser.
        self.sjTraverser = SpaceJamTraverser()

        # Make our base class wrapper that we can pass to our other classes as one simple object.
        self.base = SpaceJamBase(
            self.loader,
            self.render,
            self.clock,
            self.taskMgr,
            self.camera,
            self.accept,
            self.sjTraverser,
            self.hud,
        )

        # Game environment / enemies
        self.universe = SpaceJamUniverse(self.base)
        self.solarSystem = SpaceJamSolarSystem(self.base)
        self.enemyBaseA = SpaceJamEnemyBase(
            self.base,
            "SpaceBaseA",
            self.solarSystem.mercury.modelNode.getPos() + (8, -8, -8),
            self.solarSystem.mercury.modelNode,
            self.onBaseWasDestroyed,
        )

        if self.camera == None:
            raise AssertionError("Game did not have a valid camera!")

        # Player
        self.player = PlayerController(
            self.base,
            self.enemyBaseA.droneWasDestroyed,
            self.enemyBaseA.baseWasShot,
            self.onPlayerWasDestroyed,
        )

        # Moves the ship somewhere reasonable outside of the Sun
        self.player.modelNode.setPos((50, 60, 30))
        self.hud.addOnscreenPlayerKeyBindings()

        # Now that the player exists, our Traverser can do its thing with it.
        self.sjTraverser.preparePlayerTraverser(
            self.render, self.player.cNode, self.player.shipHull.pusher
        )

        # Finally Panda3D needs us to assign to this special cTrav on ShowBase to a Panda3D CollisionTraverser
        # We'll use the one we made in our wrapper traverser.
        self.cTrav = self.sjTraverser.ct

        # Debug tools
        self.debugActions = DebugActions(self.accept, self.player.movement)

    def onPlayerWasDestroyed(self):
        self.hud.addOrUpdateTitle("Sorry, You Lost.")

    def onBaseWasDestroyed(self):
        self.player.victoryInvincibility = True
        self.hud.addOrUpdateTitle("YOU WON SPACE JAM!!")


app = SpaceJam()
app.run()
