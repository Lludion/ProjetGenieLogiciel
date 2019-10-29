#!/usr/bin/env python3

from map_point import Map_Point
from level import Level


class Level_Sequence(Map_Point):
    
    def __init__(self):
        self.__levels = []
        
    def set_levels(self, levels):
        self.__levels = levels
        
    def get_levels(self):
        return self.__levels