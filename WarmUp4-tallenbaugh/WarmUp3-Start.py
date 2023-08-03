import math, sys, random, os
from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TextNode
from panda3d.core import Vec3, CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionNode

from direct.gui.DirectGui import *

PI = 4.0*math.atan(1.0)
DEGREEStoRADIANS = PI / 180.0
RADIANStoDEGREES = 180.0 / PI

# Set timeout for connection attempts
timeout = 1000

# Setting window properties
# props = WindowProperties()
# props.setCursorHidden(True)

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
			pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
	                pos=(0.0,-0.95), align=TextNode.ACenter, scale = .07)

class Flatland(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Post the instructions
        self.title = addTitle("SIMPLE GAME TESTING NETWORKS")
        self.inst1 = addInstructions(0.95, "[ESC]: Quit")
        self.inst2 = addInstructions(0.90, "[arrow_up]: Move Positive Y")
        self.inst3 = addInstructions(0.85, "[arrow_down]: Move Negative Y")
        self.inst4 = addInstructions(0.80, "[arrow_right]: Move Positive X")
        self.inst5 = addInstructions(0.75, "[arrow_left]: Move Negative X")
        
        base.setBackgroundColor(0,0,0)
       
        # Loading Model as 0 Point for Vector calculation (invisible at world base 0,0,0)

        # create and render fighter; create parent to be instanced to the cubes that will make the wall
        self.fighter = self.loader.loadModel('./Assets/sphere')
        self.fighter.reparentTo(self.render)
        self.fighter.setColorScale(1.0, 0, 0, 1.0)

        self.parent = self.loader.loadModel("./Assets/cube")

        x = 0
        for i in range(100):
            theta = x
            self.placeholder2 = self.render.attachNewNode('Placeholder2')
            position = Vec3(math.cos(theta), math.sin(theta), 0)
            position = position * 50
            self.placeholder2.setPos(position)
            red = 0.6 + (random.random() * 0.4)
            grn = 0.6 + (random.random() * 0.4)
            blu = 0.6 + (random.random() * 0.4)
            self.placeholder2.setColorScale(red, grn, blu, 1.0)
            self.parent.instanceTo(self.placeholder2)
            x = x + 0.06

        #Disable Mouse control over camera
        base.disableMouse()
        base.camera.setPos(0.0, 0.0, 250.0)
        base.camera.setHpr(0.0, -90.0, 0.0)
        
        # start setting key bindings
        self.accept('escape', self.quit)
        self.accept('arrow_right', self.posX, [1])
        self.accept('arrow_right-up', self.posX, [0])
        self.accept('arrow_left', self.negX, [1])
        self.accept('arrow_left-up', self.negX, [0])
        self.accept('arrow_up', self.posY, [1])
        self.accept('arrow_up-up', self.posY, [0])
        self.accept('arrow_down', self.negY, [1])
        self.accept('arrow_down-up', self.negY, [0])

        # set up for collisions -- inside the constructor
        cNode = CollisionNode('fighterC')
        cNode.addSolid(CollisionSphere(0, 0, 0, 1.05))
        self.fighterC = self.fighter.attachNewNode(cNode)

        # collisions for parent which will be instanced to all cubes
        cNode = CollisionNode('parentC')
        cNode.addSolid(CollisionSphere(0, 0, 0, 1.3))
        self.parentC = self.parent.attachNewNode(cNode)

        # show for debugging NOTICE ME
        # self.fighterC.show()
        # self.parentC.show()

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.fighterC, self.fighter)

        base.cTrav = CollisionTraverser()
        base.cTrav.addCollider(self.fighterC, self.pusher)

        base.cTrav.showCollisions(render)

    # Prepare message if server wants to quit
    def quit(self):
        ## Network contacts will go here 
        sys.exit()
    
    # methods for arrow key movement
    def posX(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvPosX, "movePosX")
        else:
            self.taskMgr.remove("movePosX")
    def mvPosX(self, task):
        self.fighter.setX(self.fighter, 0.4)
        return task.cont
    
    def negX(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvNegX, "moveNegX")
        else:
            self.taskMgr.remove("moveNegX")
    def mvNegX(self, task):
        self.fighter.setX(self.fighter, -0.4)
        return task.cont
    
    def posY(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvPosY, "movePosY")
        else:
            self.taskMgr.remove("movePosY")
    def mvPosY(self, task):
        self.fighter.setY(self.fighter, 0.4)
        return task.cont
    
    def negY(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvNegY, "moveNegY")
        else:
            self.taskMgr.remove("moveNegY")
    def mvNegY(self, task):
        self.fighter.setY(self.fighter, -0.4)
        return task.cont

        
play = Flatland()
play.run()
