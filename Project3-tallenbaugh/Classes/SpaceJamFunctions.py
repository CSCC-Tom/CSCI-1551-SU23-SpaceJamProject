from panda3d.core import Vec3


def SpawnPatternLine(count: int, origin: Vec3, direction: Vec3):
    pos_list: list[Vec3] = []
    for i in range(count):
        pos_list.append(origin + (direction[0] * i, direction[1] * i, direction[2] * i))
    return pos_list


# dir_a is the direction of each line, dir_b is the direction of each line's subsequent origin.
def SpawnPatternLineSequence(count: int, origin: Vec3, dir_a: Vec3, dir_b: Vec3):
    pos_list: list[Vec3] = []
    for i in range(count):
        line_origin = origin + (dir_b[0] * i, dir_b[1] * i, dir_b[2] * i)
        pos_list.extend(SpawnPatternLine(count, line_origin, dir_a))
    return pos_list
