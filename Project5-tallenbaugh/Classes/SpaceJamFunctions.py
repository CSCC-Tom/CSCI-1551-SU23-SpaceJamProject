from panda3d.core import Vec3


def CreateLinePatternPositionsList(count: int, origin: Vec3, direction: Vec3):
    """Creates a line of count positions starting from the origin and spaced out by the direction vector."""
    pos_list: list[Vec3] = []
    for i in range(count):
        pos_list.append(origin + (direction[0] * i, direction[1] * i, direction[2] * i))
    return pos_list


# dir_a is the direction of each line, dir_b is the direction of each line's subsequent origin.
def CreateLineOfLinePatternsPositionsList(
    count_of_lines: int,
    count_per_line: int,
    origin: Vec3,
    dir_of_each_line: Vec3,
    dir_between_line_origins: Vec3,
):
    """Creates count_of_lines lines each containing count_per_line positions. Each line points towards dir_of_each_line. Each line is dir_between_line_origins apart."""
    pos_list: list[Vec3] = []
    for i in range(count_of_lines):
        line_origin = origin + (
            dir_between_line_origins[0] * i,
            dir_between_line_origins[1] * i,
            dir_between_line_origins[2] * i,
        )
        pos_list.extend(
            CreateLinePatternPositionsList(
                count_per_line, line_origin, dir_of_each_line
            )
        )
    return pos_list
