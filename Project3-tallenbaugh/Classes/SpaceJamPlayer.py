from panda3d.core import PandaNode, Loader, NodePath
from Classes import SpaceJamClasses
from direct.task import Task
from pandac.PandaModules import Vec3
from direct.task.Task import TaskManager


class SpaceJamPlayerShip(PandaNode):
    def __init__(
        self,
        loader: Loader,
        render: NodePath,
        taskMgr: TaskManager,
        camera: NodePath,
    ):
        PandaNode.__init__(self, "Player")
        self.shipObj = SpaceJamClasses.loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            0.3,
            (0, 0, 0),
            (0.95, 0.7, 0.8, 1.0),
        )
        self.taskMgr = taskMgr
        self.render = render
        self.camera = camera

        # Add the updateCameraTask procedure to the task manager.
        self.taskMgr.add(self.updatePlayerCameraTask, "UpdateCameraTask")

        self.rotationRate = 2
        self.thrustRate = 1

        self.lookTarget = NodePath("Player Look Target")
        self.lookTarget.setPosHpr(self.shipObj.getPos(), self.shipObj.getHpr())

    def getShipPos(self):
        return self.shipObj.getPos()

    def getShipForward(self):
        return self.render.getRelativeVector(self.shipObj, Vec3(0, 1, 0))

    def getShipRight(self):
        return self.render.getRelativeVector(self.shipObj, Vec3(1, 0, 0))

    def getShipUp(self):
        return self.render.getRelativeVector(self.shipObj, Vec3(0, 0, 1))

    # HEADING
    def headingCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipHeadingCW, "rotateShipHeadingCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCW")

    def rotateShipHeadingCW(self, task: Task):
        self.lookTarget.setPos(
            self.getShipPos() + (self.getShipForward() * 50) + self.getShipRight()
        )
        self.shipObj.lookAt(self.lookTarget.getPos(), self.getShipUp())
        print("Rotate CW -- Curr Heading = " + str(self.shipObj.getH()))
        return task.cont

    def headingCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipHeadingCCW, "rotateShipHeadingCCW")
        else:
            self.taskMgr.remove("rotateShipHeadingCCW")

    def rotateShipHeadingCCW(self, task: Task):
        self.lookTarget.setPos(
            self.getShipPos() + (self.getShipForward() * 50) - self.getShipRight()
        )
        self.shipObj.lookAt(self.lookTarget.getPos(), self.getShipUp())
        print("Rotate CCW -- Curr Heading = " + str(self.shipObj.getH()))
        return task.cont

    # PITCH
    def pitchCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipPitchCW, "rotateShipPitchCW")
        else:
            self.taskMgr.remove("rotateShipPitchCW")

    def rotateShipPitchCW(self, task: Task):
        self.lookTarget.setPos(
            self.getShipPos() + (self.getShipForward() * 50) + self.getShipUp()
        )
        self.shipObj.lookAt(self.lookTarget.getPos(), self.getShipUp())
        print("Rotate CW -- Curr Pitch = " + str(self.shipObj.getP()))

        return task.cont

    def pitchCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipPitchCCW, "rotateShipPitchCCW")
        else:
            self.taskMgr.remove("rotateShipPitchCCW")

    def rotateShipPitchCCW(self, task: Task):
        self.lookTarget.setPos(
            self.getShipPos() + (self.getShipForward() * 50) - self.getShipUp()
        )
        self.shipObj.lookAt(self.lookTarget.getPos(), self.getShipUp())
        print("Rotate CW -- Curr Pitch = " + str(self.shipObj.getP()))

        return task.cont

    # ROLL
    def rollCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipRollCW, "rotateShipRollCW")
        else:
            self.taskMgr.remove("rotateShipRollCW")

    def rotateShipRollCW(self, task: Task):
        curr_r = self.shipObj.getR() % 360
        print("Rotate CW -- Curr Roll = " + str(curr_r))
        self.shipObj.setR(curr_r - self.rotationRate)
        return task.cont

    def rollCCWKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.rotateShipRollCCW, "rotateShipRollCCW")
        else:
            self.taskMgr.remove("rotateShipRollCCW")

    def rotateShipRollCCW(self, task: Task):
        curr_r = self.shipObj.getR() % 360
        print("Rotate CCW -- Curr Roll = " + str(curr_r))
        self.shipObj.setR(curr_r + self.rotationRate)
        return task.cont

    # THRUST
    def thrustKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(self.addShipThrust, "addShipThrust")
        else:
            self.taskMgr.remove("addShipThrust")

    def addShipThrust(self, task: Task):
        self.shipObj.setPos(self.shipObj.getPos() + self.getShipForward())
        # self.shipObj.setR(self.shipObj.getR() - self.rotationRate)
        return task.cont

    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task: Task):
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)
        player_pos = self.shipObj.getPos()
        player_forward = self.render.getRelativeVector(self.shipObj, Vec3(0, 6, 0))
        player_up = self.render.getRelativeVector(self.shipObj, Vec3(0, 0, 1))
        self.camera.setPos(player_pos - player_forward + player_up)
        # self.camera.headsUp(player_pos, player_up)
        # self.camera.setPos(self.camera.getPos() )
        self.camera.setHpr(self.shipObj.getHpr())
        return task.cont
