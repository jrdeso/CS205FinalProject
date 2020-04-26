import dataclasses
import enum


class PathType(enum.IntEnum):
    PATH_START = enum.auto()
    PATH_END = enum.auto()
    PATH = enum.auto()
    TOWER = enum.auto()

    @staticmethod
    def GetEnum(s):
        """
        Take a string of and get the
        respective enum.

        :param s: a string of either 'path_start', 'path', 'tower', 'path_end'
        :return: the enum corresponding to the string or -1
        """
        if s == "path_start":
            return PathType.PATH_START
        elif s == "path_end":
            return PathType.PATH_END
        elif s == "path":
            return PathType.PATH
        elif s == "tower":
            return PathType.TOWER
        return -1


@dataclasses.dataclass
class MapNode:
    __ID = 0
    pathType: int = 0
    edges: list = dataclasses.field(default_factory=list)

    def __post_init__(self, *args, **kwargs):
        self.id = MapNode.__ID
        MapNode.__ID = MapNode.__ID + 1
