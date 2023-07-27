from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider
from Classes.Player.Weapon import ShipCannon
from Classes.Player.WeaponProjectile import PhaserMissile
from Classes.Player.Movement import ShipThrusters
from Classes.Player.Input import PlayerActionHandler
from Classes.Player.GyroSensors import ShipGyroscope
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from direct.task import Task
from pandac.PandaModules import (
    CollisionHandlerPusher,
    CollisionNode,
)
from typing import Callable


class PlayerController(ModelWithSphereCollider):
    """The all-important class managing the Player object. The interface between the human player and the game! Controls the player ship and camera and maps the input."""

    def __init__(
        self,
        base: SpaceJamBase,
        player_destroyed_drone_cb: Callable[[CollisionNode], None],
    ):
        ModelWithSphereCollider.__init__(
            self, base, "./Assets/TheBorg/theBorg.egg", base.render, "Player"
        )

        # Set up our gyro module. (Expected by other modules.)
        self.shipGyro = ShipGyroscope(base.render, self.modelNode)

        # Set up our movement module. (Expected by input.)
        self.movement = ShipThrusters(self.shipGyro)

        # Phaser / Missile Weapon
        self.cannon = ShipCannon(
            base,
            self.shipGyro,
            self.onPlayerMissileHitEnemyDrone,
        )
        self.destroyEnemyDroneCallback = player_destroyed_drone_cb
        # Set up our input, which requires both the movement and cannon module to work.
        self.input = PlayerActionHandler(base, self.movement, self.cannon)

        # Ship model is huge. Not ideal; scaling it down for now.
        self.modelNode.setScale(0.1)

        self.replaceTextureOnModel(
            base.loader, "./Assets/Planets/angryPlanet.jpg", (0.95, 0.7, 0.8, 1.0)
        )
        self.loader = base.loader
        self.taskMgr = base.taskMgr
        self.scene_node = base.render
        self.camera = base.camera

        # Add the updateCameraTask procedure to the task manager.
        self.taskMgr.add(self.updatePlayerCameraTask, "UpdateCameraTask")

        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cNode, self.modelNode)

    # CAMERA TASK
    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task: Task):
        """Defines a procedure to move the camera every frame. Puts it directly behind + above the player ship, and aligns the rotation with the player ship. The rotation of the ship itself is controlled by the input action events."""

        # Examples. 'task.time' can help you smooth out from slight differences in the amount of time since the last call of the task.
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)

        shipPos = self.shipGyro.getShipPos()
        # Negative times forward = backward
        behindOffset = self.shipGyro.getShipForward() * -24
        aboveOffset = self.shipGyro.getShipUp() * 4

        # Move the camera behind, and a little above, the ship. Could space this out over multiple task updates for a more "drifty-feeling" camera.
        self.camera.setPos(shipPos + behindOffset + aboveOffset)

        # Make the camera match the ship's rotation exactly. (Could use headsUp or lookAt similarly, if you want the camera to look at the player rather than look where the player is looking.)
        self.camera.setHpr(self.modelNode.getHpr())
        return task.cont

    def onPlayerMissileHitEnemyDrone(
        self, missile: PhaserMissile, target_drone_cNode: CollisionNode
    ):
        print(
            "A " + missile.modelColliderNode.name + " hit a " + target_drone_cNode.name
        )
        # When we hit an enemy drone, we want:
        # - Reload the ship (ship cannon handles this on the way up to this callback)
        # - Destroy the drone (we will request it from the EnemyBase)
        self.destroyEnemyDroneCallback(target_drone_cNode)
