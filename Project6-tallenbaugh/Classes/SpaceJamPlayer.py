from panda3d.core import Loader, NodePath
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider
from Classes.Player.Weapon import ShipCannon
from Classes.Player.WeaponProjectile import PhaserMissile
from Classes.Player.Movement import ShipThrusters
from Classes.Player.Input import PlayerActionHandler
from Classes.Enemy.EnemyDrone import EnemyBaseDrone
from direct.task import Task
from pandac.PandaModules import (
    Vec3,
    CollisionHandler,
    CollisionHandlerPusher,
    CollisionNode,
)
from direct.task.Task import TaskManager
from typing import Callable


class PlayerController(ModelWithSphereCollider):
    """The all-important class managing the Player object. The interface between the human player and the game! Controls the player ship and camera and maps the input."""

    def __init__(
        self,
        loader: Loader,
        scene_node: NodePath,
        taskMgr: TaskManager,
        camera: NodePath,
        input_accept: Callable[[str, Callable, []], None],
        start_handling_collisions_cb: Callable[[NodePath, CollisionHandler], None],
        stop_handling_collisions_cb: Callable[[NodePath], None],
    ):
        ModelWithSphereCollider.__init__(
            self, loader, "./Assets/TheBorg/theBorg.egg", scene_node, "Player"
        )

        # Set up our movement module. (Expected by input.)
        self.movement = ShipThrusters(
            self.modelNode,
            self.getShipPos,
            self.getShipHpr,
            self.getShipForward,
            self.getShipUp,
            self.getShipRight,
        )
        # Phaser / Missile Weapon
        self.cannon = ShipCannon(
            loader,
            scene_node,
            self.getShipPos,
            self.getShipForward,
            start_handling_collisions_cb,
            stop_handling_collisions_cb,
            self.onPlayerMissileHitEnemyDrone,
        )
        # Set up our input, which requires both the movement and cannon module to work.
        self.input = PlayerActionHandler(
            input_accept, self.movement, self.cannon, taskMgr
        )

        # Ship model is huge. Not ideal; scaling it down for now.
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

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cNode, self.modelNode)

    # CONVENIENCE FUNCTIONS to make other functions more concise and self-describing.
    def getShipPos(self):
        """Convenience to get current ship position in space."""
        return self.modelNode.getPos()

    def getShipHpr(self):
        """Convenience to get current ship (absolute) rotation in space"""
        return self.modelNode.getHpr()

    def getShipForward(self):
        """Convenience to get the vector representing the current forward direction from the ship's perspective"""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(0, 1, 0))

    def getShipRight(self):
        """Convenience to get the vector representing the current right-hand direction from the ship's perspective."""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(1, 0, 0))

    def getShipUp(self):
        """Convenience to get the vector representing the current upward direction from the ship's perspective."""
        return self.scene_node.getRelativeVector(self.modelNode, Vec3(0, 0, 1))

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

    def onPlayerMissileHitEnemyDrone(
        self, missile: PhaserMissile, target_drone_cNode: CollisionNode
    ):
        print(
            "A " + missile.modelColliderNode.name + " hit a " + target_drone_cNode.name
        )
