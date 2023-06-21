import sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode
from Classes import SpaceJamClasses


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


class SpaceJam(ShowBase):
    # Prepare message if server wants to quit
    def quit(self):
        ## Network contacts will go here

        sys.exit()

    def __init__(self):
        ShowBase.__init__(self)

        self.title = addTitle("SPACE JAM CLASS EXAMPLE")

        self.universe = SpaceJamClasses.SpaceJamUniverse(self.loader, self.render)
        self.planets = SpaceJamClasses.SpaceJamPlanets(self.loader, self.render)

        # Disable Mouse control over camera
        # self.disableMouse()
        # self.camera.setPos(3000.0, 0, 0)
        # ShowBase.use_drive(self)
        # print("Camera position is ")

        # start setting key bindings
        self.accept("escape", self.quit)


app = SpaceJam()
app.run()
