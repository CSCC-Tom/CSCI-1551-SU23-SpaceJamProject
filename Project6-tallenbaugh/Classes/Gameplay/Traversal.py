from panda3d.core import NodePath
from pandac.PandaModules import CollisionTraverser, CollisionHandler
from Classes.SpaceJamPlayer import PlayerController


class SpaceJamTraverser:
    """Class to handle core traversal and collisions for the game."""

    def preparePlayerTraverser(self, render: NodePath, player: PlayerController):
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(render)
        self.cTrav.addCollider(player.cNode, player.pusher)
        self.cTrav.showCollisions(render)

    def startTrackingCollisionsForHandler(
        self, collider_node: NodePath, collision_handler: CollisionHandler
    ):
        self.cTrav.addCollider(collider_node, collision_handler)

    def stopTrackingCollisionsForHandler(self, collider_node: NodePath):
        self.cTrav.removeCollider(collider_node)
