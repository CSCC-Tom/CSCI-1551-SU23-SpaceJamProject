from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider


class SpaceJamUniverse(ModelWithSphereCollider):
    """ModelWithSphereCollider representing the Universe (skybox)"""

    def __init__(self, base: SpaceJamBase):
        ModelWithSphereCollider.__init__(
            self,
            base,
            "./Assets/Universe/Universe.obj",
            base.render,
            "Universe",
            True,
        )
        self.modelNode.setScale(90000)
