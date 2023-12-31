from panda3d.core import NodePath
from direct.task import Task
from Classes.Player.GyroSensors import ShipGyroscope

# Can play with these values to change how it feels to fly by default
DEFAULT_PLAYER_ROTATION_RATE = 2
DEFAULT_PLAYER_THRUST_RATE = 1


class ShipThrusters:
    """Class to help manage ship movement"""

    rotationRate = DEFAULT_PLAYER_ROTATION_RATE
    thrustRate = DEFAULT_PLAYER_THRUST_RATE

    def __init__(
        self,
        ship_gyro: ShipGyroscope,
    ):
        self.getShipPos = ship_gyro.getShipPos
        self.getShipHpr = ship_gyro.getShipHpr
        self.getShipForward = ship_gyro.getShipForward
        self.getShipUp = ship_gyro.getShipUp
        self.getShipRight = ship_gyro.getShipRight
        # empty-object target to help the ship stay oriented in desired rotations without fancy Euler logic
        self.lookTarget = NodePath("Player Look Target")
        self.lookTarget.setPosHpr(self.getShipPos(), self.getShipHpr())

        self.shipModelNode = ship_gyro.shipNode

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
        self.shipModelNode.lookAt(self.lookTarget.getPos(), self.getShipUp())

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
        curr_r = self.shipModelNode.getR() % 360
        # print("Rotate CW -- Curr Roll = " + str(curr_r))
        self.shipModelNode.setR(curr_r - self.rotationRate)
        return task.cont

    def rotateShipRollCW(self, task: Task):
        """Makes ship rotate roll counter-clockwise."""
        # Note that since the lookTarget is always directly ahead of the player, there is no need to touch it.
        curr_r = self.shipModelNode.getR() % 360
        # print("Rotate CCW -- Curr Roll = " + str(curr_r))
        self.shipModelNode.setR(curr_r + self.rotationRate)
        return task.cont

    def addShipThrust(self, task: Task):
        """Makes the ship go a little bit forward. No acceleration or velocity (yet), just directly dragging it through space."""
        self.shipModelNode.setPos(
            self.getShipPos() + (self.getShipForward() * self.thrustRate)
        )
        # print("Player at " + str(self.modelNode.getPos()))
        return task.cont
