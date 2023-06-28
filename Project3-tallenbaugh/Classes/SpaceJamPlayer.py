from panda3d.core import PandaNode
from Classes import SpaceJamClasses
from direct.task import Task
from pandac.PandaModules import Vec3


class SpaceJamPlayerShip(PandaNode):
    def assignPlayerKeyBindings(self, space_jam_game):
        # start setting key bindings
        space_jam_game.accept("arrow_right", self.headingClockwiseKeyEvent, [1])
        space_jam_game.accept("arrow_right-up", self.headingClockwiseKeyEvent, [0])

    def __init__(self, space_jam_game, loader, render, taskMgr, camera):
        PandaNode.__init__(self, "Player")
        self.shipObj = SpaceJamClasses.loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            0.3,
            0,
            0,
            0,
            0.95,
            0.7,
            0.8,
        )
        self.taskMgr = taskMgr
        self.render = render
        self.camera = camera

        self.assignPlayerKeyBindings(space_jam_game)

        # Add the updateCameraTask procedure to the task manager.
        self.taskMgr.add(self.updatePlayerCameraTask, "UpdateCameraTask")

    def headingClockwiseKeyEvent(self, keydown):
        if keydown:
            self.taskMgr.add(
                self.rotateShipHeadingClockwise, "rotateShipHeadingClockwise"
            )
        else:
            self.taskMgr.remove("rotateShipHeadingClockwise")

    def rotateShipHeadingClockwise(self, task):
        rate = 2
        self.shipObj.setH(self.shipObj.getH() - rate)
        return task.cont

    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task):
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)
        player_pos = self.shipObj.getPos()
        player_forward = self.render.getRelativeVector(self.shipObj, Vec3(0, 6, 0))
        player_up = self.render.getRelativeVector(self.shipObj, Vec3(0, 0, 1))
        self.camera.setPos(player_pos - player_forward)
        self.camera.lookAt(player_pos)
        self.camera.setPos(self.camera.getPos() + player_up)
        # self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
