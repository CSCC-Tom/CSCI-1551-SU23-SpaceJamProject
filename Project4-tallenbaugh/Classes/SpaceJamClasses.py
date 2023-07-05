from panda3d.core import PandaNode, Loader, NodePath, Texture, Vec3, LColor
from Classes import SpaceJamFunctions


def loadAndAddModelObject(
    loader,
    parent: NodePath,
    model_asset_path: str,
    scale: float = 1.0,
    pos: Vec3 = (0.0, 0.0, 0.0),
    col: LColor = (1.0, 1.0, 1.0, 1.0),
) -> NodePath:
    """loadAndAddModelObject is a function that anything in the game can use to create a NodePath for itself out of a model.

    This NodePath should be saved to a self.variable if intended for dynamic logic"""
    new_node_path: NodePath = loader.loadModel(model_asset_path)

    if not isinstance(new_node_path, NodePath):
        raise AssertionError(
            "loader.loadModel("
            + model_asset_path
            + ") did not return a proper PandaNode!"
        )
    new_node_path.reparentTo(parent)
    new_node_path.setScale(scale)
    new_node_path.setColorScale(col)
    new_node_path.setPos(pos)

    return new_node_path


def swapTextureForObject(loader, obj: NodePath, texture_path: str):
    texture: Texture = loader.loadTexture(texture_path)

    if not isinstance(texture, Texture):
        raise AssertionError(
            "swapTextureForObject passed texture_path of "
            + texture_path
            + ", loader.loadTexture could not load a valid Texture from it!"
        )

    obj.setTexture(texture)


class SpaceJamUniverse(PandaNode):
    def __init__(self, loader: Loader, scene_node: NodePath):
        PandaNode.__init__(self, "Universe")

        self.universe = loadAndAddModelObject(
            loader, scene_node, "./Assets/Universe/Universe.obj", 90000
        )
        self.something = loadAndAddModelObject(
            loader, scene_node, "./Assets/Planets/protoPlanet.obj", 30, (0, 0, 99000)
        )
        self.sun = loadAndAddModelObject(
            loader,
            self.universe,
            "./Assets/Planets/protoPlanet.obj",
            2000,
            (3000, 3000, 3000),
            (0.95, 0.7, 0.1, 1.0),
        )


class SpaceJamPlanets(PandaNode):
    def __init__(self, loader: Loader, render: NodePath):
        PandaNode.__init__(self, "Planets")

        self.mercury = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            7,
            (30, 20, 10),
            (1.0, 0.75, 0.75, 1.0),
        )
        self.bbq = loadAndAddModelObject(
            loader, render, "./Assets/Planets/protoPlanet.obj", 14, (50, 40, 30)
        )

        swapTextureForObject(loader, self.mercury, "./Assets/Planets/geomPatterns2.png")
        swapTextureForObject(loader, self.bbq, "./Assets/Planets/bbq.jpeg")


class SpaceJamBase(PandaNode):
    def __init__(self, loader: Loader, render: NodePath, pos: Vec3):
        PandaNode.__init__(self, "SpaceBase")

        self.homebase = loadAndAddModelObject(
            loader, render, "./Assets/Universe/Universe.obj", 1, pos
        )
        self.defenders: list[SpaceJamDefender] = []
        self.spawnDefenders(loader, render, 100, 0, (1, 0, 0, 1))
        self.spawnDefenders(loader, render, 100, 1, (0, 1, 0, 1))

    def spawnDefenders(
        self,
        loader: Loader,
        render: NodePath,
        count: int,
        pattern: int,
        color_tint: LColor,
    ):
        if pattern == 0:
            def_positions = SpaceJamFunctions.SpawnPatternLine(
                count, self.homebase.getPos(), (1, 1, -1)
            )
        elif pattern == 1:
            def_positions = SpaceJamFunctions.SpawnPatternLineSequence(
                count, self.homebase.getPos(), (-1, 0, 1), (1, -1, -1)
            )

        for pos in def_positions:
            self.defenders.append(SpaceJamDefender(loader, render, pos, color_tint))


class SpaceJamDefender(PandaNode):
    def __init__(self, loader: Loader, render: NodePath, pos: Vec3, col_tint: LColor):
        PandaNode.__init__(self, "SpaceBaseDefender")

        self.obj = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            0.5,  # 0.05
            pos,
            col_tint,
        )
