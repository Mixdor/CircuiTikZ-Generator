from __future__ import annotations

from PyQt6.QtCore import QPointF

from objects.Tools import ObjTool


class ObjComponent:

    def __init__(self, num:int, built_tool:ObjTool, positions:ObjPosition,
                 rotation:float, scales:ObjScales, label:str, colors:ObjColors, draws:list):

        self.num : int = num
        self.built_tool : ObjTool = built_tool
        self.positions : ObjPosition = positions
        self.rotation : float = rotation
        self.scales : ObjScales = scales
        self.label : str = label
        self.colors : ObjColors = colors
        self.draws : list = draws


class ObjPosition:

    def __init__(self, start_point:QPointF|None, middle_point:QPointF, end_point:QPointF|None):
        self.start_point : QPointF = start_point
        self.middle_point : QPointF = middle_point
        self.end_point : QPointF = end_point

    def __int__(self, middle_point:QPointF):
        self.middle_point: QPointF = middle_point


class ObjScales:

    def __init__(self, x_scale:int, y_scale:int):
        self.x_scale : int = x_scale
        self.y_scale : int = y_scale


class ObjColors:

    def __init__(self, stroke:str, filled:str):
        self.stroke : str = stroke
        self.filled : str = filled
