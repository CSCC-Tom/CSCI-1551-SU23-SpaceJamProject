from panda3d.core import PandaNode
from Classes.Environment.Planet import SpaceJamPlanet
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class SpaceJamSolarSystem(PandaNode):
    """PandaNode container of all the Planets in the Universe. Currently contains Sun, Mercury, and BBQ"""

    def __init__(self, base: SpaceJamBase):
        super(SpaceJamSolarSystem, self).__init__("Solar System")

        self.sun = SpaceJamPlanet(
            base,
            "./Assets/Planets/protoPlanet.obj",
            "Sun",
            (0, 0, 0),
            20,
        )
        self.sun.replaceTextureOnModel(
            base.loader, "./Assets/Planets/geomPatterns2.png"
        )

        self.mercury = SpaceJamPlanet(
            base,
            "./Assets/Planets/protoPlanet.obj",
            "Mercury",
            (30, 20, 10),
            7,
        )
        self.mercury.replaceTextureOnModel(
            base.loader, "./Assets/Planets/geomPatterns2.png"
        )
        self.mercury.modelNode.setColorScale((1.0, 0.75, 0.75, 1.0))

        self.bbq = SpaceJamPlanet(
            base,
            "./Assets/Planets/protoPlanet.obj",
            "BBQ",
            (50, 40, 30),
            14,
        )
        self.bbq.replaceTextureOnModel(base.loader, "./Assets/Planets/bbq.jpeg")
