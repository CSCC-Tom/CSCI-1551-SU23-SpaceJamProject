from panda3d.core import NodePath, Vec3, CollisionNode
from Classes.GameObjects.GameModel import ModelObject
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.GameObjects.ModelWithCollider import (
    ModelWithCapsuleCollider,
)
from Classes.Gameplay.OrbitingLogic import OrbitType, SimpleCircleOrbitTask
from Classes.Enemy.EnemyDefenderSpawner import SpawningPattern, DefenderDroneSpawner


class SpaceJamEnemyBase(ModelWithCapsuleCollider):
    """SphereCollidableObject that also manages a swarm of Defenders"""

    dronesDestroyed = 0

    def __init__(
        self,
        base: SpaceJamBase,
        unique_name: str,
        pos: Vec3,
        orbit_around: NodePath,
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
            self.modelNode, 100, SpawningPattern.LineOfLines, (0, 1, 0, 1)
        )

        self.defenderSpawner.spawnTraveler(unique_name)

        # print("Space Jam Base placed at " + str(pos))
        self.cNode.setTag("enemy", "base")

        self.orbitTask = SimpleCircleOrbitTask(
            base, self.modelNode, orbit_around, 10, True, OrbitType.XY, True
        )

    def droneWasDestroyed(self, droneCNode: CollisionNode):
        for d in self.defenderSpawner.spawned:
            if d.cNode.name == droneCNode.name:
                self.dronesDestroyed += 1
                # Removes from list of defenders, but does not yet "destroy"
                self.defenderSpawner.spawned.remove(d)
                # Let the drone destroy itself (allows managed particle effect)
                d.beginDeath()
                print("Drones Destroyed: " + str(self.dronesDestroyed))
                return
