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


class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.title = addTitle("SPACE JAM CLASS EXAMPLE")


app = SpaceJam()
app.run()
