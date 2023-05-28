# -*- encoding: utf-8 -*-


from os.path import abspath
from enum import Enum


class PointType(Enum):

    space = 0
    start = 1
    end = 2
    wall = 3

class AStar(object):

    def __init__(self, data_path, max=20):
        self.max = max
        self.data_path = data_path
        map_reader = MapReader(self.data_path)
        self.map = map_reader.read()
    
    def get_info(self):
        wall = []
        for line in enumerate(self.map):
            for item in enumerate(line[1]):
                pos = [item[0], line[0]]
                if item[1] == PointType.start:
                    start = pos
                elif item[1] == PointType.end:
                    end = pos
                elif item[1] == PointType.wall:
                    wall.append(pos)
        return start, end, wall, [item[0] + 1, line[0] + 1]
    
    def get_sides(self, p, wall, size, footprints):
        sides = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                mp = [p[0] + i, p[1] + j]
                if ((not mp in wall) and
                    0 <= mp[0] < size[0] and
                    0 <= mp[1] < size[1] and
                    (not i == j == 0) and
                    (not mp in footprints)
                ):
                    sides.append(mp)
        return sides

    def euclidean(self, p1, p2):
        return (abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2) ** (1 / 2)
    
    def getfootprints(self):
        return range(1, 6)
    
    def find_way(self):
        start, end, wall, size = self.get_info()
        minway = []
        for footprintslength in self.getfootprints():
            trys = 0
            p = start
            way = []
            footprints = []
            while p != end:
                min_f = [float('inf'), p]
                for mp in self.get_sides(p, wall, size, footprints):
                    h = self.euclidean(mp, end)
                    g = self.euclidean(mp, p)
                    f = h + g

                    if f < min_f[0]:
                        min_f = (f, mp)
                footprints.append(p)
                if len(footprints) == footprintslength + 1: del footprints[0]
                p = min_f[1]
                way.append(p)
                if trys >= self.max:
                    way = None
                    break
                trys += 1
            if way != None:
                if minway == []:
                    minway = way
                elif len(minway) > len(way):
                    minway = way
        return minway

class MapReader(object):

    def __init__(self, data_path):
        self.data_path = data_path

    def read(self):
        with open(self.data_path, mode='r', encoding='utf-8') as file:
            data = file.read()
        
        return self.build_map(data)
    
    def build_map(self, data):
        map = []
        data = data.split('\n')

        for line in enumerate(data):
            map.append([])
            for item in line[1]:
                    point = PointType(int(item))
                    map[line[0]].append(point)
        return map

def rp(s, old, new):
    for item in zip(old, new):
        s = s.replace(*item)
    return s


if __name__ == '__main__':
    path = abspath('map.txt')
    with open(path, 'r', encoding='utf-8') as f:
        s = rp(f.read(), ['0', '1', '2', '3'], ['口', '始', '终', '墙'])
        print(s)
    astar = AStar(path)
    print(w := astar.find_way(), len(w))