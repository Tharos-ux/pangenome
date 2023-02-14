"Tools to represent GFA format"
from enum import Enum
from re import sub
from tharospytools import overload


class Orientation(Enum):
    "Describes the way a node is read"
    FORWARD = '+'
    REVERSE = '-'


class GfaStyle(Enum):
    "Describes the different possible formats"
    RGFA = 'rGFA'
    GFA1 = 'GFA1'
    GFA1_1 = 'GFA1.1'
    GFA1_2 = 'GFA1.2'
    GFA2 = 'GFA2'


class LineType(Enum):
    "Modelizes the line type in GFA format by the meaning of first char of sequence"
    HEADER = 'H'
    SEGMENT = 'S'
    LINE = 'L'
    CONTAINMENT = 'C'
    PATH = 'P'
    WALK = 'W'
    JUMP = 'J'


class Segment():
    pass


class Line():
    pass


class Containment():
    pass


class Path():
    pass


class Walk():
    pass


class Header():
    pass


class Jump():
    pass


class Record():

    def __init__(self, line: str, gfa_type: str) -> None:
        self.gfastyle: GfaStyle = GfaStyle(gfa_type)
        self.linetype: LineType = LineType(line[0])
        self.__class__ = Walk
        self.__subinit__(line.split())

    @overload(Walk, list)
    def __subinit__(self, datas) -> None:
        if self.gfastyle in [GfaStyle.RGFA, GfaStyle.GFA1]:
            raise ValueError(
                f"Incompatible version format, W-lines vere added in GFA1.1 and were absent from {gfa_style}.")
        self.idf = datas[1]
        self.origin = int(datas[2])
        self.name = datas[3]
        self.target = datas[4]
        self.length = datas[5]
        self.path = [
            (
                node[1:],
                Orientation(node[0])
            )
            for node in datas[6].replace('>', ',+').replace('<', ',-')[1:].split(',')
        ]

    @overload(Segment, list)
    def __subinit__(self, datas: list) -> None:
        self.name = sub('\D', '', datas[1])
        # self.seq = datas[2]
        self.length = len(datas[2])
        if self.gfa_style == GfaStyle.RGFA:
            self.origin = int(datas[6][5:])

    @overload(Line, list)
    def __subinit__(self, datas: list) -> None:
        if self.gfa_style == GfaStyle.RGFA:
            self.origin = int(datas[6][5:])
        self.start = sub('\D', '', datas[1])
        self.end = sub('\D', '', datas[3])
        self.orientation = f"{datas[2]}/{datas[4]}"

    @overload(Containment, list)
    def __subinit__(self, datas: list) -> None:
        if self.gfa_style == GfaStyle.RGFA:
            raise ValueError(
                f"Incompatible version format, C-lines vere added in GFA1 and were absent from {self.gfa_style}.")

    @overload(Header, list)
    def __subinit__(self, datas: list) -> None:
        if self.gfa_style == GfaStyle.RGFA:
            raise ValueError(
                f"Incompatible version format, H-lines vere added in GFA1 and were absent from {gfa_style}.")
        self.version = datas[1][5:]

    @overload(Path, list)
    def __subinit__(self, datas: list) -> None:
        if self.gfa_style == GfaStyle.RGFA:
            raise ValueError(
                f"Incompatible version format, P-lines vere added in GFA1 and were absent from {gfa_style}.")
        self.name = datas[1]
        self.path = [
            (
                node[:-1],
                Orientation(node[-1])
            )
            for node in datas[2].split(',')
        ]

    @overload(Jump, list)
    def __subinit__(self, datas: list) -> None:
        if self.gfa_style in [GfaStyle.RGFA, GfaStyle.GFA1, GfaStyle.GFA1_1]:
            raise ValueError(
                f"Incompatible version format, J-lines vere added in GFA1.2 and were absent from {gfa_style}.")
        raise NotImplementedError


print(Record('S	259122	AAT	SN:Z:SeqBt1#28	SO:i:46871782	SR:i:0', 'GFA1.1'))
