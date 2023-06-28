from panda3d.core import PandaNode


def loadAndAddModelObject(
    loader,
    render,
    obj_path,
    scale=1,
    pos_x=0.0,
    pos_y=0.0,
    pos_z=0.0,
    col_r=1.0,
    col_g=1.0,
    col_b=1.0,
    col_a=1.0,
):
    new_obj = loader.loadModel(obj_path)
    new_obj.setScale(scale)
    new_obj.setColorScale(col_r, col_g, col_b, col_a)
    new_obj.reparentTo(render)
    new_obj.setPos(pos_x, pos_y, pos_z)
    return new_obj


def swapTextureForObject(loader, obj, texture_path):
    texture = loader.loadTexture(texture_path)
    obj.setTexture(texture)


class SpaceJamUniverse(PandaNode):
    def __init__(self, loader, render):
        PandaNode.__init__(self, "Universe")

        self.universe = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Universe/Universe.obj",
            90000,
            0,
            0,
            0,
        )
        self.sun = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            2000,
            3000,
            3000,
            3000,
            0.95,
            0.7,
            0.1,
        )


class SpaceJamPlanets(PandaNode):
    def __init__(self, loader, render):
        PandaNode.__init__(self, "Planets")

        self.mercury = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            7,
            30,
            20,
            10,
            1.0,
            0.75,
            0.75,
        )
        self.bbq = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            14,
            50,
            40,
            30,
        )

        swapTextureForObject(loader, self.mercury, "./Assets/Planets/geomPatterns2.png")
        swapTextureForObject(loader, self.bbq, "./Assets/Planets/bbq.jpeg")


class SpaceJamBase(PandaNode):
    def __init__(self, loader, render, pos):
        PandaNode.__init__(self, "SpaceBase")

        self.homebase = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Universe/Universe.obj",
            1,
            pos[0],
            pos[1],
            pos[2],
        )
        self.spawnDefenders(loader, render, 100, 0)

    def spawnDefenders(self, loader, render, count, pattern):
        self.defender = SpaceJamDefender(
            loader, render, self.homebase.getPos() + (1, -1, -1), (1, 0, 0, 1)
        )


class SpaceJamDefender(PandaNode):
    def __init__(self, loader, render, pos, col_tint):
        PandaNode.__init__(self, "SpaceBaseDefender")

        self.obj = loadAndAddModelObject(
            loader,
            render,
            "./Assets/Planets/protoPlanet.obj",
            0.05,
            pos[0],
            pos[1],
            pos[2],
            col_tint[0],
            col_tint[1],
            col_tint[2],
            col_tint[3],
        )
