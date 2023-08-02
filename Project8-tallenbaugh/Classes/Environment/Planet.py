from panda3d.core import Vec3
from Classes.GameObjects.ModelWithCollider import (
    ModelWithSphereCollider,
)
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class SpaceJamPlanet(ModelWithSphereCollider):
    """ModelWithSphereCollider representing a Planet"""

    def __init__(
        self,
        base: SpaceJamBase,
        model_path: str,
        node_name: str,
        position: Vec3,
        scale: float,
    ):
        ModelWithSphereCollider.__init__(self, base, model_path, base.render, node_name)

        # Note position of 0 above to make sure the collider matches visual position, and then both are moved by moving the parent modelNode.
        self.modelNode.setPos(position)
        # Note scale of 1 above to make sure the collider matches visual size, and THEN we scale both up together by scaling the parent modelNode.
        self.modelNode.setScale(scale)
        self.cNode.setTag("neutral", "neutral")
