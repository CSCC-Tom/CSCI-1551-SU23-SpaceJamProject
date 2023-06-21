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
    def __init__(self):
        PandaNode.__init__(self, "Universe")
