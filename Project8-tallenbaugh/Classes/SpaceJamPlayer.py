from Classes.Player.Collider import ShipHull
from Classes.Player.Weapon import ShipCannon
from Classes.Player.WeaponProjectile import PhaserMissile
from Classes.Player.Movement import ShipThrusters
from Classes.Player.Input import PlayerActionHandler
from Classes.Player.GyroSensors import ShipGyroscope
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.GameObjects.DestructibleShip import DestructibleShip
from direct.task import Task
from pandac.PandaModules import CollisionNode, CollisionEntry
from typing import Callable


class PlayerController(DestructibleShip):
    """The all-important class managing the Player object. The interface between the human player and the game! Controls the player ship and camera and maps the input."""

    victoryInvincibility = False

    def __init__(
        self,
        base: SpaceJamBase,
        player_destroyed_drone_cb: Callable[[CollisionNode], None],
        player_shot_base_cb: Callable[[], None],
        player_was_destroyed_cb: Callable[[], None],
    ):
        DestructibleShip.__init__(
            self,
            base,
            "./Assets/TheBorg/theBorg.egg",
            base.render,
            (0, 0, 0),
            (1, 1, 1, 1),
            "Player",
        )
        self.timePerDeathStep = 3.0
        self.destroyEnemyDroneCallback = player_destroyed_drone_cb
        self.shotEnemyBaseCallback = player_shot_base_cb
        self.onDestroyedCB = player_was_destroyed_cb
        self.shipHull = ShipHull(
            self.modelNode, self.cNode, self.onPlayerShipCollidedWithObject
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
            self.onPlayerMissileHitEnemyBase,
        )
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

    # CAMERA TASK
    # Define a procedure to move the camera.
    def updatePlayerCameraTask(self, task: Task):
        """Defines a procedure to move the camera every frame. Puts it directly behind + above the player ship, and aligns the rotation with the player ship. The rotation of the ship itself is controlled by the input action events."""

        if not self.modelNode:
            # We're already dead and the modelNode was destroyed
            self.taskMgr.remove("UpdateCameraTask")
            return task.cont

        # Examples. 'task.time' can help you smooth out from slight differences in the amount of time since the last call of the task.
        # angleDegrees = task.time * 6.0
        # angleRadians = angleDegrees * (pi / 180.0)

        shipPos = self.shipGyro.getShipPos()
        # Negative times forward = backward
        behindOffset = self.shipGyro.getShipForward() * -24
        aboveOffset = self.shipGyro.getShipUp() * 4

        if self.shipHull.hitpoints <= 0:
            # During death but not yet dead
            timeSinceDeath = 1.0 + (self.clock.getRealTime() - self.timeOfDeath)
            invTSD = 1.0 / timeSinceDeath
            self.camera.setPos(
                shipPos
                + (behindOffset * timeSinceDeath)
                + (aboveOffset * timeSinceDeath)
            )
            self.modelNode.setColor((1 * invTSD, 0.5 * invTSD, 0.5 * invTSD, 0))
            self.camera.lookAt(self.modelNode)
        else:
            # Move the camera behind, and a little above, the ship. Could space this out over multiple task updates for a more "drifty-feeling" camera.
            self.camera.setPos(shipPos + behindOffset + aboveOffset)
            # Make the camera match the ship's rotation exactly. (Could use headsUp or lookAt similarly, if you want the camera to look at the player rather than look where the player is looking.)
            self.camera.setHpr(self.modelNode.getHpr())
        return task.cont

    def onPlayerMissileHitEnemyDrone(
        self, missile: PhaserMissile, target_drone_cNode: CollisionNode
    ):
        # print("Your Missile hit a " + target_drone_cNode.name)
        # When we hit an enemy drone, we want:
        # - Reload the ship (ship cannon handles this on the way up to this callback)
        # - Destroy the drone (we will request it from the EnemyBase)
        self.destroyEnemyDroneCallback(target_drone_cNode)

    def onPlayerMissileHitEnemyBase(
        self, missile: PhaserMissile, target_base_cNode: CollisionNode
    ):
        # print("Your Missile hit a " + target_base_cNode.name)
        # When we hit an enemy drone, we want:
        # - Reload the ship (ship cannon handles this on the way up to this callback)
        # - Destroy the drone (we will request it from the EnemyBase)
        self.shotEnemyBaseCallback()

    def onPlayerShipCollidedWithObject(self, entry: CollisionEntry):
        if self.victoryInvincibility == True:
            return

        self.shipHull.hitpoints = self.shipHull.hitpoints - 1
        if self.shipHull.hitpoints > 0:
            self.modelNode.setColor((1, 0.8, 0.8, 1))
            print("The ship got hurt running into a " + entry.into_node.name + "!")
        else:
            self.modelNode.setColor((1, 0.5, 0.5, 0))
            print("The ship ran into a " + entry.into_node.name + " and died!")
            self.beginDeath()
            self.cannon.disable()
            self.input.disable()
            self.onDestroyedCB()
