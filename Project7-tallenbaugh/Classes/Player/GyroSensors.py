from panda3d.core import NodePath
from pandac.PandaModules import Vec3


class ShipGyroscope:
    """Class responsible for helping the ship orient itself in space. Mostly just convenience functions."""

    def __init__(self, scene_node: NodePath, ship_model_node: NodePath):
        self.sceneNode = scene_node
        self.shipNode = ship_model_node

    # CONVENIENCE FUNCTIONS to make other functions more concise and self-describing.
    def getShipPos(self):
        """Convenience to get current ship position in space."""
        return self.shipNode.getPos()

    def getShipHpr(self):
        """Convenience to get current ship (absolute) rotation in space"""
        return self.shipNode.getHpr()

    def getShipForward(self):
        """Convenience to get the vector representing the current forward direction from the ship's perspective"""
        return self.sceneNode.getRelativeVector(self.shipNode, Vec3(0, 1, 0))

    def getShipRight(self):
        """Convenience to get the vector representing the current right-hand direction from the ship's perspective."""
        return self.sceneNode.getRelativeVector(self.shipNode, Vec3(1, 0, 0))

    def getShipUp(self):
        """Convenience to get the vector representing the current upward direction from the ship's perspective."""
        return self.sceneNode.getRelativeVector(self.shipNode, Vec3(0, 0, 1))
