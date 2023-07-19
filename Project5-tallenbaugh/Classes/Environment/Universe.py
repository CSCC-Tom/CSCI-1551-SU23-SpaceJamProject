from panda3d.core import Loader, NodePath
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider


class SpaceJamUniverse(ModelWithSphereCollider):
    """ModelWithSphereCollider representing the Universe (skybox)"""

    def __init__(self, loader: Loader, scene_node: NodePath):
        ModelWithSphereCollider.__init__(
            self, loader, "./Assets/Universe/Universe.obj", scene_node, "Universe", True
        )
        self.modelNode.setScale(90000)
