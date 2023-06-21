import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode


# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(
        text=text,
        style=1,
        fg=(1, 1, 1, 1),
        pos=(0.0, -0.95),
        align=TextNode.ACenter,
        scale=0.07,
    )


def loadAndAddModelObject(
    self,
    obj_path,
    scale=1,
    pos_x=0.0,
    pos_y=0.0,
    pos_z=0.0,
    col_r=1.0,
    col_g=1.0,
    col_b=1.0,
    col_a=1.0,
):
    new_obj = self.loader.loadModel(obj_path)
    new_obj.setScale(scale)
    new_obj.setColorScale(1.0, 1.0, 1.0, 1.0)
    new_obj.reparentTo(self.render)
    new_obj.setPos(pos_x, pos_y, pos_z)
    return new_obj


def swapTextureForObject(self, obj, texture_path):
    texture = self.loader.loadTexture(texture_path)
    obj.setTexture(texture)


class SpaceJam(ShowBase):
    # Prepare message if server wants to quit
    def quit(self):
        ## Network contacts will go here

        sys.exit()

    def __init__(self):
        ShowBase.__init__(self)

        self.title = addTitle("SPACE JAM CLASS EXAMPLE")

        self.universe = loadAndAddModelObject(
            self, "./Assets/Universe/Universe.obj", 90000, 0, 0, 0
        )

        self.sun = loadAndAddModelObject(
            self,
            "./Assets/Planets/protoPlanet.obj",
            2000,
            3000,
            3000,
            3000,
        )

        self.mercury = loadAndAddModelObject(
            self,
            "./Assets/Planets/protoPlanet.obj",
            7,
            30,
            20,
            10,
        )
        swapTextureForObject(self, self.mercury, "./Assets/Planets/geomPatterns2.png")

        # Disable Mouse control over camera
        # self.disableMouse()
        # self.camera.setPos(3000.0, 0, 0)
        # ShowBase.use_drive(self)
        # print("Camera position is ")

        # start setting key bindings
        self.accept("escape", self.quit)


app = SpaceJam()
app.run()
