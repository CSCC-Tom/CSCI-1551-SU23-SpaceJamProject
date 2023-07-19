from panda3d.core import Loader, PandaNode, NodePath
from Classes.Environment.Planet import SpaceJamPlanet


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
