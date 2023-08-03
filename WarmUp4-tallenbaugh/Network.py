from panda3d.core import NodePath

MSG_NONE = 0
MSG_AUTH = 1
MSG_POS = 2
MSG_QUIT = 3
MSG_CQUIT = 4
MSG_CPOS = 5


def getNodePathStats(p: NodePath):
    return [p.getX(), p.getY(), p.getZ(), p.getH(), p.getP(), p.getR()]
