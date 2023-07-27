from panda3d.core import Loader, NodePath, ClockObject
from typing import Callable
from direct.task.Task import TaskManager
from Classes.Gameplay.Traversal import SpaceJamTraverser


class SpaceJamBase:
    """Class to wrap around the useful ShowBase constructs so we can pass them down in simpler ways"""

    def __init__(
        self,
        loader: Loader,
        render: NodePath,
        clock: ClockObject,
        taskMgr: TaskManager,
        camera: NodePath,
        # Callable is a 'helper type' you can import.
        # Here it's saying that "accept" is a function that takes a string, another function, and some list, and returns None.
        # That is actually more accurate than what SpaceJam.accept is designed to take, so the typing is able to guide us.
        accept: Callable[[str, Callable, []], None],
        sjTraverser: SpaceJamTraverser,
    ):
        self.loader = loader
        self.render = render
        self.clock = clock
        self.taskMgr = taskMgr
        self.camera = camera
        self.accept = accept
        self.sjTraverser = sjTraverser
