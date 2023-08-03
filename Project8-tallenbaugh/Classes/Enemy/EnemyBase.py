from typing import Callable
from panda3d.core import NodePath, Vec3, CollisionNode
from Classes.GameObjects.GameModel import ModelObject
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.GameObjects.ModelWithCollider import (
    ModelWithCapsuleCollider,
)
from Classes.Gameplay.OrbitingLogic import DynamicCircleOrbitTask
from Classes.Enemy.EnemyDefenderSpawner import SpawningPattern, DefenderDroneSpawner


class SpaceJamEnemyBase(ModelWithCapsuleCollider):
    """SphereCollidableObject that also manages a swarm of Defenders"""

    dronesDestroyed = 0
    baseHitpoints = 5
    baseIsDestroyed = False

    def __init__(
        self,
        base: SpaceJamBase,
        unique_name: str,
        pos: Vec3,
        orbit_around: NodePath,
        base_was_destroyed_cb: Callable[[], None],
    ):
        ModelWithCapsuleCollider.__init__(
            self,
            base,
            "./Assets/Universe/Universe.obj",
            base.render,
            unique_name,
            (0, 0, 0),
            (0.75, 0, 0),
        )
        self.baseModelB = ModelObject(
            base.loader,
            "./Assets/Universe/Universe.obj",
            self.modelNode,
            unique_name + "B",
        )
        self.baseModelB.modelNode.setPos((0.75, 0, 0))
        self.modelNode.setPos(pos)
        self.modelNode.setScale(1.5)

        self.defenderSpawner = DefenderDroneSpawner(base, self.modelNode)
        self.defenderSpawner.spawnDefenders(
            self.modelNode, 100, SpawningPattern.Line, (1, 0, 0, 1)
        )
        self.defenderSpawner.spawnDefenders(
            self.modelNode, 20, SpawningPattern.LineOfLines, (0, 1, 0, 1)
        )

        self.defenderSpawner.spawnTraveler(unique_name)

        # print("Space Jam Base placed at " + str(pos))
        self.cNode.setTag("enemy", "base")

        self.orbitTask = DynamicCircleOrbitTask(
            base, self.modelNode, orbit_around, 10, True
        )
        self.gameHUD = base.hud
        self.baseDestroyedCB = base_was_destroyed_cb

    def droneWasDestroyed(self, droneCNode: CollisionNode):
        for d in self.defenderSpawner.spawned:
            if d.cNode.name == droneCNode.name:
                self.dronesDestroyed = self.dronesDestroyed + 1
                # Removes from list of defenders, but does not yet "destroy"
                self.defenderSpawner.spawned.remove(d)
                # Let the drone destroy itself (allows managed particle effect)
                d.beginDeath()
                print("Destroyed a Drone!")
                if self.baseHitpoints > 0:
                    self.orbitTask.next_orbit_duration = (
                        self.orbitTask.next_orbit_duration + 1
                    )
                    if self.dronesDestroyed >= 30:
                        msg = "SPACE JAM : Destroy the Base!!"
                    elif self.dronesDestroyed == 29:
                        msg = "SPACE JAM : Destroy 1 More Drone!"
                    else:
                        dronesLeft = str(30 - self.dronesDestroyed)
                        msg = "SPACE JAM : Destroy " + dronesLeft + " More Drones!"
                    self.gameHUD.addOrUpdateTitle(msg)
                # print("Drones Destroyed: " + str(self.dronesDestroyed))
                return

    def baseWasShot(self):
        if self.dronesDestroyed < 30:
            print(
                "The Base's shields are too strong... Destroy "
                + str(30 - self.dronesDestroyed)
                + " more Drone(s)!"
            )
            return  # No damage can be done

        if self.baseHitpoints > 0:
            print("You hit the Base!!")
            self.baseHitpoints = self.baseHitpoints - 1

        if self.baseHitpoints > 0:
            self.gameHUD.addOrUpdateTitle(
                "SPACE JAM : Destroy the Base!! ("
                + str((10 - self.baseHitpoints) * 10)
                + "%)"
            )
        elif self.baseIsDestroyed == False:
            self.baseIsDestroyed = True
            self.cNode.removeNode()
            self.orbitTask.stopOrbiting()
            for s in self.defenderSpawner.spawned:
                self.defenderSpawner.spawned.remove(s)
                s.beginDeath()
            self.baseDestroyedCB()
