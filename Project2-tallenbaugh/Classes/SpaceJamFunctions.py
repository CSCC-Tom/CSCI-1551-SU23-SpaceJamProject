def SpawnPatternLine(count, origin, direction):
    pos_list = []
    for i in range(count):
        pos_list.append(origin + (direction[0] * i, direction[1] * i, direction[2] * i))
    return pos_list


# dir_a is the direction of each line, dir_b is the direction of each line's subsequent origin.
def SpawnPatternLineSequence(count, origin, dir_a, dir_b):
    pos_list = []
    for i in range(count):
        line_origin = origin + (dir_b[0] * i, dir_b[1] * i, dir_b[2] * i)
        pos_list.extend(SpawnPatternLine(count, line_origin, dir_a))
    return pos_list
