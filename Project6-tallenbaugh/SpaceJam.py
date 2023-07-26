import sys
from direct.showbase.ShowBase import ShowBase
from Classes.HUD.HeadsUpDisplay import SpaceJamHeadsUpDisplay
from Classes.SpaceJamPlayer import PlayerController
from Classes.Gameplay.Traversal import SpaceJamTraverser
from Classes.Environment.Universe import SpaceJamUniverse
from Classes.Environment.SolarSystem import SpaceJamSolarSystem
from Classes.Enemy.EnemyBase import SpaceJamEnemyBase
from Classes.Debug.SpaceJamDebug import DebugActions


def quit():
    """Prepare message if server wants to quit"""
    ## Network contacts will go here
    sys.exit()


class SpaceJam(ShowBase):
    """Base class for the whole Space Jam game, that interfaces with the ShowBase of the Panda3D library."""

    def assignCoreKeyBindings(self):
        """Key bindings that involve very core game functions. Currently maps the escape key to the Quit function."""
        self.accept("escape", quit)
        self.hud.addOnscreenCoreKeyBindings()

    def __init__(self):
        ShowBase.__init__(self)

        # Onscreen text
        self.hud = SpaceJamHeadsUpDisplay()

        self.hud.addTitle("SPACE JAM CLASS EXAMPLE")

        self.assignCoreKeyBindings()
        self.enableParticles()  # <-- Particles won't work without this

        # Collisions and traversal
        # Saving this to its own special variable because it is our wrapper around the true traverser.
        self.sjTraverser = SpaceJamTraverser()

        # Game environment / enemies
        self.universe = SpaceJamUniverse(self.loader, self.render)
        self.solarSystem = SpaceJamSolarSystem(self.loader, self.render)
        self.baseA = SpaceJamEnemyBase(
            self.loader,
            self.render,
            "SpaceBaseA",
            self.solarSystem.mercury.modelNode.getPos() + (8, -8, -8),
        )

        if self.camera == None:
            raise AssertionError("Game did not have a valid camera!")

        # Player
        self.player = PlayerController(
            self.loader,
            self.render,
            self.taskMgr,
            self.camera,
            self.accept,
            self.sjTraverser.startTrackingCollisionsForHandler,
            self.sjTraverser.stopTrackingCollisionsForHandler,
            self.baseA.droneWasDestroyed,
        )

        # Moves the ship somewhere reasonable outside of the Sun
        self.player.modelNode.setPos((50, 60, 30))
        self.hud.addOnscreenPlayerKeyBindings()

        # Now that the player exists, our Traverser can do its thing with it.
        self.sjTraverser.preparePlayerTraverser(self.render, self.player)

        # Finally Panda3D needs us to assign to this special cTrav on ShowBase to a Panda3D CollisionTraverser
        # We'll use the one we made in our wrapper traverser.
        self.cTrav = self.sjTraverser.ct

        # Debug tools
        self.debugActions = DebugActions(self.accept, self.player.movement)


app = SpaceJam()
app.run()
