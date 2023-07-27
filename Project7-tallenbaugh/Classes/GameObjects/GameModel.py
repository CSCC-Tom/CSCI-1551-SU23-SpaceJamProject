from panda3d.core import Loader, PandaNode, NodePath, Texture, Vec3, LColor


class ModelObject(PandaNode):
    """PandaNode object with a primary NodePath called modelNode, that also offers functions to load and modify the model."""

    def __init__(
        self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str
    ):
        self.modelNode = self.loadAndAddModelNodePath(loader, parent_node, model_path)
        self.modelNode.setName(node_name)

    def loadAndAddModelNodePath(
        self,
        loader: Loader,
        parent: NodePath,
        model_asset_path: str,
        scale: float = 1.0,
        pos: Vec3 = (0.0, 0.0, 0.0),
    ) -> NodePath:
        """A function that any ObjectWithModel in the game can use to create a NodePath for itself out of a model.

        This NodePath should be saved to a self.variable if intended for dynamic logic
        """
        print(
            "GameModel passed loader: "
            + str(loader)
            + " to load model "
            + model_asset_path
        )
        self.modelNode: NodePath = loader.loadModel(model_asset_path)

        if not isinstance(self.modelNode, NodePath):
            raise AssertionError(
                "loader.loadModel("
                + model_asset_path
                + ") did not return a proper PandaNode!"
            )
        self.modelNode.reparentTo(parent)
        self.modelNode.setScale(scale)
        self.modelNode.setPos(pos)

        return self.modelNode

    def replaceTextureOnModel(
        self, loader: Loader, texture_path: str, col: LColor = (1.0, 1.0, 1.0, 1.0)
    ):
        """Shared function to swap the texture of the modelNode of a ObjectWithModel if desired"""
        texture: Texture = loader.loadTexture(texture_path)

        if not isinstance(texture, Texture):
            raise AssertionError(
                "swapTextureForObject passed texture_path of "
                + texture_path
                + ", loader.loadTexture could not load a valid Texture from it!"
            )

        self.modelNode.setTexture(texture)
        self.modelNode.setColorScale(col)
