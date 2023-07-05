from panda3d.core import PandaNode, Loader, NodePath, Vec3, LColor
from Classes import SpaceJamFunctions, BaseClasses, CollisionBaseClasses

# Script containing primarily "end leaf" classes for SpaceJam that are not inherited by anything, and are generally small.
# (Large classes belong in their own script files!)


class SpaceJamUniverse(BaseClasses.ObjectWithModel):
    """ObjectWithModel representing the Universe (skybox)"""

    def __init__(self, loader: Loader, scene_node: NodePath):
        super(SpaceJamUniverse, self).__init__(
            loader, "./Assets/Universe/Universe.obj", scene_node, "Universe"
        )
        self.modelNode.setScale(90000)


class SpaceJamPlanet(CollisionBaseClasses.SphereCollidableObject):
    """SphereCollidableObject representing a Planet"""

    def __init__(
        self,
        loader,
        model_path: str,
        parent_node: NodePath,
        node_name: str,
        position: Vec3,
        scale: float,
    ):
        super(SpaceJamPlanet, self).__init__(
            loader, model_path, parent_node, node_name, (0, 0, 0), 1
        )
        # Note position of 0 above to make sure the collider matches visual position, and then both are moved by moving the parent modelNode.
        self.modelNode.setPos(position)
        # Note scale of 1 above to make sure the collider matches visual size, and THEN we scale both up together by scaling the parent modelNode.
        self.modelNode.setScale(scale)


class SpaceJamSolarSystem(PandaNode):
    """PandaNode container of all the Planets in the Universe. Currently contains Sun, Mercury, and BBQ"""

    def __init__(self, loader: Loader, parent_node: NodePath):
        super(SpaceJamSolarSystem, self).__init__("Solar System")

        self.sun = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "Sun",
            (0, 0, 0),
            20,
        )
        self.sun.replaceTextureOnModel(loader, "./Assets/Planets/geomPatterns2.png")

        self.mercury = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "Mercury",
            (30, 20, 10),
            7,
        )
        self.mercury.replaceTextureOnModel(loader, "./Assets/Planets/geomPatterns2.png")
        self.mercury.modelNode.setColorScale((1.0, 0.75, 0.75, 1.0))

        self.bbq = SpaceJamPlanet(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "BBQ",
            (50, 40, 30),
            14,
        )
        self.bbq.replaceTextureOnModel(loader, "./Assets/Planets/bbq.jpeg")


class SpaceJamBase(CollisionBaseClasses.SphereCollidableObject):
    """SphereCollidableObject that also manages a swarm of Defenders"""

    def __init__(self, loader: Loader, parent_node: NodePath, pos: Vec3):
        super(SpaceJamBase, self).__init__(
            loader,
            "./Assets/Universe/Universe.obj",
            parent_node,
            "SpaceBase",
        )

        self.modelNode.setPos(pos)
        self.modelNode.setScale(1.5)
        self.defenders: list[SpaceJamDefender] = []
        self.spawnDefenders(loader, self.modelNode, 100, 0, (1, 0, 0, 1))
        self.spawnDefenders(loader, self.modelNode, 100, 1, (0, 1, 0, 1))

    def spawnDefenders(
        self,
        loader: Loader,
        parent_node: NodePath,
        count: int,
        pattern: int,
        color_tint: LColor,
    ):
        """Spawns the defenders around the base by way of the given pattern. pattern 0 is a line, pattern 1 is a line of lines. Spawned defenders are added to the base's list."""
        if pattern == 0:
            def_positions = SpaceJamFunctions.CreateLinePatternPositionsList(
                count, Vec3(0, 0, 0), Vec3(1, 1, -1)
            )
        elif pattern == 1:
            def_positions = SpaceJamFunctions.CreateLineOfLinePatternsPositionsList(
                count, count, Vec3(0, 0, 0), Vec3(-1, 0, 1), Vec3(1, -1, -1)
            )

        for pos in def_positions:
            self.defenders.append(
                SpaceJamDefender(loader, parent_node, pos, color_tint)
            )


class SpaceJamDefender(CollisionBaseClasses.SphereCollidableObject):
    """SphereCollidableObject spawned and managed by a Base"""

    def __init__(
        self, loader: Loader, parent_node: NodePath, pos: Vec3, col_tint: LColor
    ):
        super(SpaceJamDefender, self).__init__(
            loader,
            "./Assets/Planets/protoPlanet.obj",
            parent_node,
            "SpaceBaseDefender",
        )
        self.modelNode.setScale(0.5)
        self.modelNode.setPos(pos)
        self.modelNode.setColorScale(col_tint)
