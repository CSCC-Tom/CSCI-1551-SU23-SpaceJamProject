from panda3d.core import Loader, NodePath
from Classes import BaseClasses, CollisionBaseClasses, PlayerPhaser
from direct.task import Task
from pandac.PandaModules import Vec3
from direct.task.Task import TaskManager
from direct.interval.LerpInterval import LerpPosInterval

DEFAULT_PLAYER_ROTATION_RATE = 2
DEFAULT_PLAYER_THRUST_RATE = 1


class SpaceJamPlayerShip(BaseClasses.ModelObject, CollisionBaseClasses.SphereCollider):
    """The all-important class managing the Player object. The interface between the human player and the game! Controls the player ship and camera and maps the input."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        taskMgr: TaskManager,
        camera: NodePath,
    ):
        BaseClasses.ModelObject.__init__(
            self, loader, "./Assets/TheBorg/theBorg.egg", scene_node, "Player"
        )
        CollisionBaseClasses.SphereCollider.__init__(self, self.modelNode, "Player")

        self.modelNode.setScale(0.1)

        self.replaceTextureOnModel(
            loader, "./Assets/Planets/angryPlanet.jpg", (0.95, 0.7, 0.8, 1.0)
        )
        self.loader = loader
        self.taskMgr = taskMgr
        self.scene_node = scene_node
        self.camera = camera

        # Add the updateCameraTask procedure to the task manager.
        self.taskMgr.add(self.updatePlayerCameraTask, "UpdateCameraTask")

        # Can play with these values to change how it feels to fly
        self.rotationRate = DEFAULT_PLAYER_ROTATION_RATE
        self.thrustRate = DEFAULT_PLAYER_THRUST_RATE

        # empty-object target to help the ship stay oriented in desired rotations without fancy Euler logic
        self.lookTarget = NodePath("Player Look Target")
        self.lookTarget.setPosHpr(self.modelNode.getPos(), self.modelNode.getHpr())

        # Phaser / Missile Attributes
        self.missilesReady = 1

    # CONVENIENCE FUNCTIONS to make other functions more concise and self-describing.
    def getShipPos(self):
        """Convenience to get current ship position in space."""
        return self.modelNode.getPos()

    def getShipForward(self):
        """Convenience to get the vector representing the current forward direction from the ship's perspective"""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(0, 1, 0))

    def getShipRight(self):
        """Convenience to get the vector representing the current right-hand direction from the ship's perspective."""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(1, 0, 0))

    def getShipUp(self):
        """Convenience to get the vector representing the current upward direction from the ship's perspective."""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(0, 0, 1))

    # KEY EVENT INPUT HELPERS
    # used to turn one-time "keyup" and "keydown" events into a continuous task called during every "frame" of the game where the button is held down.
    def headingCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipHeadingCW, "rotateShipHeadingCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCW")

    def headingCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipHeadingCCW, "rotateShipHeadingCCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCCW")

    def pitchCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipPitchCW, "rotateShipPitchCW")
        else:
            self.taskMgr.remove("rotateShipPitchCW")

    def pitchCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipPitchCCW, "rotateShipPitchCCW")
        else:
            self.taskMgr.remove("rotateShipPitchCCW")

    def rollCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipRollCCW, "rotateShipRollCCW")
        else:
            self.taskMgr.remove("rotateShipRollCCW")

    def rollCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipRollCW, "rotateShipRollCW")
        else:
            self.taskMgr.remove("rotateShipRollCW")

    def thrustKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.addShipThrust, "addShipThrust")
        else:
            self.taskMgr.remove("addShipThrust")

    # MOVEMENT ACTION HELPERS
    # Called every frame by the Key Event Input Helper tasks
    # Rotation functions are moving an empty invisible "lookTarget" object and making the ship look at it.
    # The advantage of this over get/setH/P/R is that the raw HPR functions are based on absolute world space, and the math is kind of hard.
    # Physically moving an invisible object and looking at it, requires less math for the programmer than doing fancy quaternion-based operations.
    # You are free to implement your rotations in whatever way you prefer, as long as they're reasonable.

    def adjustShipLookTarget(self, up_amount: float, right_amount: float):
        """Helper function to adjust the ship's look target. Uses rotationRate; use -1.0 to 1.0 to set up_ and right_amount between a full down/left and a full up/right turn"""
        self.lookTarget.setPos(
            self.getShipPos()
            + (self.getShipForward() * 50)
            + (self.getShipUp() * up_amount * self.rotationRate)
            + (self.getShipRight() * right_amount * self.rotationRate)
        )

    def lookAtShipTarget(self):
        """Helper function to look at the ship's look target while maintaining current ship up direction"""
        self.modelNode.lookAt(self.lookTarget.getPos(), self.getShipUp())

    def rotateShipHeadingCW(self, task: Task):
        """Makes ship rotate heading clockwise, or to the right."""
        self.adjustShipLookTarget(0, 1)
        self.lookAtShipTarget()
        # print("Rotate CW -- Curr Heading = " + str(self.modelNode.getH()))
        return task.cont

    def rotateShipHeadingCCW(self, task: Task):
        """Makes ship rotate heading counter-clockwise, or to the left."""
        self.adjustShipLookTarget(0, -1)
        self.lookAtShipTarget()
        # print("Rotate CCW -- Curr Heading = " + str(self.modelNode.getH()))
        return task.cont

    def rotateShipPitchCW(self, task: Task):
        """Makes ship rotate pitch clockwise, or upwards."""
        self.adjustShipLookTarget(1, 0)
        self.lookAtShipTarget()
        # print("Rotate CW -- Curr Pitch = " + str(self.modelNode.getP()))
        return task.cont

    def rotateShipPitchCCW(self, task: Task):
        """Makes ship rotate pitch counter-clockwise, or downwards."""
        self.adjustShipLookTarget(-1, 0)
        self.lookAtShipTarget()
        # print("Rotate CW -- Curr Pitch = " + str(self.modelNode.getP()))
        return task.cont

    def rotateShipRollCCW(self, task: Task):
        """Makes ship rotate roll clockwise."""
        # Note that since the lookTarget is always directly ahead of the player, there is no need to touch it.
        curr_r = self.modelNode.getR() % 360
        # print("Rotate CW -- Curr Roll = " + str(curr_r))
        self.modelNode.setR(curr_r - self.rotationRate)
        return task.cont

    def rotateShipRollCW(self, task: Task):
        """Makes ship rotate roll counter-clockwise."""
        # Note that since the lookTarget is always directly ahead of the player, there is no need to touch it.
        curr_r = self.modelNode.getR() % 360
        # print("Rotate CCW -- Curr Roll = " + str(curr_r))
        self.modelNode.setR(curr_r + self.rotationRate)
        return task.cont

    def addShipThrust(self, task: Task):
        """Makes the ship go a little bit forward. No acceleration or velocity (yet), just directly dragging it through space."""
        self.modelNode.setPos(
            self.modelNode.getPos() + (self.getShipForward() * self.thrustRate)
        )
        # print("Player at " + str(self.modelNode.getPos()))
        return task.cont

    # CAMERA TASK
    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task: Task):
        """Defines a procedure to move the camera every frame. Puts it directly behind + above the player ship, and aligns the rotation with the player ship. The rotation of the ship itself is controlled by the input action events."""

        # Examples. 'task.time' can help you smooth out from slight differences in the amount of time since the last call of the task.
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)

        # Move the camera behind, and a little above, the ship. Could space this out over multiple task updates for a more "drifty-feeling" camera.
        self.camera.setPos(
            self.getShipPos() - (self.getShipForward() * 24) + (self.getShipUp() * 4)
        )

        # Make the camera match the ship's rotation exactly. (Could use headsUp or lookAt similarly, if you want the camera to look at the player rather than look where the player is looking.)
        self.camera.setHpr(self.modelNode.getHpr())
        return task.cont

    # MISSILE / PHASER STUFF
    def fireMissileIfReady(self):
        """If self.missilesReady > 0, then we prep and spawn and kick off a missile/phaser"""
        if self.missilesReady > 0:
            self.activeMissile = PlayerPhaser.PlayerPhaser(self.loader, self.scene_node)
            missileStartPos = self.modelNode.getPos() + (self.getShipForward() * 5)
            self.activeMissile.modelNode.setPos(missileStartPos)
            missileTargetPos = self.modelNode.getPos() + (self.getShipForward() * 500)
            self.missilesReady = self.missilesReady - 1
            self.activeMissile.fireInterval = LerpPosInterval(
                self.activeMissile.modelNode,
                2,
                missileTargetPos,
                missileStartPos,
                None,
                "noBlend",
                1,
                1,
                "missileFireInterval",
            )
            self.activeMissile.fireInterval.start()
