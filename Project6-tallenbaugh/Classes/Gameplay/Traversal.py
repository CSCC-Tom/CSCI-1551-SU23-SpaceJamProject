from panda3d.core import NodePath
from pandac.PandaModules import CollisionTraverser, CollisionHandler
from Classes.SpaceJamPlayer import PlayerController


class SpaceJamTraverser:
    """Wrapper class around Panda3D CollisionTraverser to handle our game's core traversal and collisions."""

    def preparePlayerTraverser(self, render: NodePath, player: PlayerController):
        self.ct = CollisionTraverser()
        self.ct.traverse(render)
        self.ct.addCollider(player.cNode, player.pusher)
        self.ct.showCollisions(render)

    def startTrackingCollisionsForHandler(
        self, collider_node: NodePath, collision_handler: CollisionHandler
    ):
        self.ct.addCollider(collider_node, collision_handler)

    def stopTrackingCollisionsForHandler(self, collider_node: NodePath):
        self.ct.removeCollider(collider_node)
