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

    def headingClockwiseKeyEvent(self, keydown: int):
        if keydown:
            self.taskMgr.add(
                self.rotateShipHeadingClockwise, "rotateShipHeadingClockwise"
            )
        else:
            self.taskMgr.remove("rotateShipHeadingClockwise")

    def rotateShipHeadingClockwise(self, task: Task):
        rate = 2
        self.shipObj.setH(self.shipObj.getH() - rate)
        return task.cont

    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task: Task):
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)
        player_pos = self.shipObj.getPos()
        player_forward = self.render.getRelativeVector(self.shipObj, Vec3(0, 6, 0))
        player_up = self.render.getRelativeVector(self.shipObj, Vec3(0, 0, 1))
        self.camera.setPos(player_pos - player_forward)
        self.camera.lookAt(player_pos)
        self.camera.setPos(self.camera.getPos() + player_up)
        # self.camera.setHpr(angleDegrees, 0, 0)
        return task.cont
