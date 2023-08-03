import math, sys, random, os
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TextNode
from panda3d.core import (
    Vec3,
    CollisionTraverser,
    CollisionHandlerPusher,
    CollisionSphere,
    CollisionNode,
    QueuedConnectionManager,
    QueuedConnectionListener,
    QueuedConnectionReader,
    ConnectionWriter,
    PointerToConnection,
    NetAddress,
    NetDatagram,
    DatagramIterator,
)

from direct.gui.DirectGui import *

from Network import MSG_AUTH, MSG_POS, MSG_QUIT, MSG_CQUIT, MSG_CPOS, getNodePathStats


PI = 4.0 * math.atan(1.0)
DEGREEStoRADIANS = PI / 180.0
RADIANStoDEGREES = 180.0 / PI

# Set timeout for connection attempts
timeout = 1000

# Setting window properties
# props = WindowProperties()
# props.setCursorHidden(True)


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(
        text=msg,
        style=1,
        fg=(1, 1, 1, 1),
        pos=(-1.3, pos),
        align=TextNode.ALeft,
        scale=0.05,
    )


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

        self.setBackgroundColor(0, 0, 0)

        # Loading Model as 0 Point for Vector calculation (invisible at world base 0,0,0)

        # create and render fighter; create parent to be instanced to the cubes that will make the wall
        self.fighter = self.loader.loadModel("./Assets/sphere")
        self.fighter.reparentTo(self.render)
        self.fighter.setColorScale(1.0, 0, 0, 1.0)

        self.parent = self.loader.loadModel("./Assets/cube")

        x = 0
        for i in range(100):
            theta = x
            self.placeholder2 = self.render.attachNewNode("Placeholder2")
            position = Vec3(math.cos(theta), math.sin(theta), 0)
            position = position * 50
            self.placeholder2.setPos(position)
            red = 0.6 + (random.random() * 0.4)
            grn = 0.6 + (random.random() * 0.4)
            blu = 0.6 + (random.random() * 0.4)
            self.placeholder2.setColorScale(red, grn, blu, 1.0)
            self.parent.instanceTo(self.placeholder2)
            x = x + 0.06

        # Disable Mouse control over camera
        self.disableMouse()
        self.camera.setPos(0.0, 0.0, 250.0)
        self.camera.setHpr(0.0, -90.0, 0.0)

        # start setting key bindings
        self.accept("escape", self.quit)
        self.accept("arrow_right", self.posX, [1])
        self.accept("arrow_right-up", self.posX, [0])
        self.accept("arrow_left", self.negX, [1])
        self.accept("arrow_left-up", self.negX, [0])
        self.accept("arrow_up", self.posY, [1])
        self.accept("arrow_up-up", self.posY, [0])
        self.accept("arrow_down", self.negY, [1])
        self.accept("arrow_down-up", self.negY, [0])

        # set up for collisions -- inside the constructor
        self.cNode = CollisionNode("fighterC")
        self.cNode.addSolid(CollisionSphere(0, 0, 0, 1.05))
        self.fighterC = self.fighter.attachNewNode(self.cNode)

        # collisions for parent which will be instanced to all cubes
        cNode = CollisionNode("parentC")
        cNode.addSolid(CollisionSphere(0, 0, 0, 1.3))
        self.parentC = self.parent.attachNewNode(cNode)

        # show for debugging NOTICE ME
        # self.fighterC.show()
        # self.parentC.show()

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.fighterC, self.fighter)

        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(self.fighterC, self.pusher)

        self.cTrav.showCollisions(self.render)

        self.initNetworkServer()

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
        self.moved = True
        return task.cont

    def negX(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvNegX, "moveNegX")
        else:
            self.taskMgr.remove("moveNegX")

    def mvNegX(self, task):
        self.fighter.setX(self.fighter, -0.4)
        self.moved = True
        return task.cont

    def posY(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvPosY, "movePosY")
        else:
            self.taskMgr.remove("movePosY")

    def mvPosY(self, task):
        self.fighter.setY(self.fighter, 0.4)
        self.moved = True
        return task.cont

    def negY(self, keydown):
        if keydown:
            self.taskMgr.add(self.mvNegY, "moveNegY")
        else:
            self.taskMgr.remove("moveNegY")

    def mvNegY(self, task):
        self.fighter.setY(self.fighter, -0.4)
        self.moved = True
        return task.cont

    def tskListenerPolling(self, task):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            netAddress = NetAddress()
            newConnection = PointerToConnection()

            if self.cListener.getNewConnection(rendezvous, netAddress, newConnection):
                newConnection = newConnection.p()
                self.activeConnections.append(newConnection)  # Remember connection
                self.cReader.addConnection(newConnection)  # Begin reading connection
        return task.cont

    def tskReaderPolling(self, task):
        if self.cReader.dataAvailable():
            datagram = NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                self.receiveMsgFromClient(datagram)

        if self.moved == True:
            for conn in self.Clients.keys():
                if conn != self.tcpSocket:
                    # Only send to clients, not to self.
                    self.cWriter.send(self.datagramPosMsg(), conn)

        return task.cont

    def initClientFighter(self, playerID, conn, pos, hpr):
        clientFighter = self.loader.loadModel("./Assets/cube")
        clientFighter.reparentTo(self.render)
        clientFighter.setColorScale(0, 0, 1.0, 1.0)
        self.clientCNode = CollisionNode("clientFighterC" + playerID)
        self.clientCNode.addSolid(CollisionSphere(0, 0, 0, 1.05))
        clientFighter.attachNewNode(self.clientCNode)
        clientFighter.setPos(pos)
        clientFighter.setHpr(hpr)

        self.Clients[conn] = playerID
        self.PlayerList[playerID] = [pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2]]
        self.Models[playerID] = clientFighter
        self.CollSpheres[playerID] = self.clientCNode.getSolid(0)
        self.CollNodes[playerID] = self.clientCNode

    def deleteClientFighter(self, playerID, conn):
        self.Clients.pop(conn)
        self.PlayerList.pop(playerID)
        self.Models.pop(playerID).removeNode()
        self.CollSpheres.pop(playerID)
        self.CollNodes.pop(playerID)

    def receiveMsgFromClient(self, datagram: NetDatagram):
        myIterator = DatagramIterator(datagram)
        msgID = myIterator.getUint8()
        msg_player_id = myIterator.getString()
        if msgID == MSG_AUTH:
            print("AUTH from " + str(datagram.getConnection()))
            self.initClientFighter(
                msg_player_id,
                datagram.getConnection(),
                (
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                ),
                (
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                ),
            )
            self.cWriter.send(self.datagramPosMsg(), datagram.getConnection())
        elif msgID == MSG_CPOS:
            print("CPOS from " + str(datagram.getConnection()))
            self.Models[msg_player_id].setPos(
                (
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                )
            )
            self.Models[msg_player_id].setHpr(
                (
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                    myIterator.getFloat64(),
                )
            )
        elif msgID == MSG_CQUIT:
            print("CQUIT from " + str(datagram.getConnection()))
            self.deleteClientFighter(msg_player_id, datagram.getConnection())

    def datagramPosMsg(self):
        posMsg = NetDatagram()
        posMsg.addUint8(MSG_POS)
        pos = self.fighter.getPos()
        hpr = self.fighter.getHpr()
        posMsg.addFloat64(pos[0])
        posMsg.addFloat64(pos[1])
        posMsg.addFloat64(pos[2])
        posMsg.addFloat64(hpr[0])
        posMsg.addFloat64(hpr[1])
        posMsg.addFloat64(hpr[2])
        return posMsg

    def initNetworkServer(self):
        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

        self.activeConnections = []  # We'll want to keep track of these later

        self.myID = "BigKahuna"
        self.port_address = 9099  # No-other TCP/IP services are using this port
        self.backlog = (
            1000  # If we ignore 1,000 connection attempts, something is wrong!
        )
        self.tcpSocket = self.cManager.openTCPServerRendezvous(
            self.port_address, self.backlog
        )

        self.cListener.addConnection(self.tcpSocket)

        self.moved = False

        # Python dictionaries to hold data
        self.Clients = {}  # PlayerID by Connection
        self.PlayerList = {}  # Player Stats by PlayerID
        self.Models = {}  # Models by PlayerID
        self.CollSpheres = {}  # CollisionSpheres by PlayerID
        self.CollNodes = {}  # CollisionNodes by PlayerID

        self.taskMgr.add(self.tskListenerPolling, "Poll the connection listener", -39)
        self.taskMgr.add(self.tskReaderPolling, "Poll the connection reader", -40)

        self.Clients[self.tcpSocket] = self.myID
        self.PlayerList[self.myID] = getNodePathStats(self.fighter)
        self.Models[self.myID] = self.fighter
        self.CollSpheres[self.myID] = self.cNode.getSolid(0)
        self.CollNodes[self.myID] = self.cNode


play = Flatland()
play.run()
