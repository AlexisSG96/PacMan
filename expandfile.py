"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import os


class ExpandFile:
    def __init__(self, srcfile, expandby=2):
        dirext = os.path.splitext(srcfile)   # tuple of dir + ext
        self.srcfile = srcfile
        self.dstfile = dirext[0] + '_expanded' + dirext[1]
        print('dstfile is: ' + self.dstfile)
        self.expand(expandby)

    def __str__(self): return 'ExpandMaze(src=' + self.srcfile + ', dst=' + self.dstfile + ')'

    def expand(self, expandby):
        k = expandby
        with open(self.srcfile, 'r') as src:
            rows = src.readlines()

        rows_kx = []
        with open(self.dstfile, 'w') as dst:
            rows_kx.append([])
            for row in rows:
                for i in range(k):
                    rows_kx.append(row)

            rows_cols_kx = []
            for row in rows_kx:
                for col in row:
                    rows_cols_kx += col
                    if col != '\n':
                        rows_cols_kx += (k - 1) * col

            dst.writelines(rows_cols_kx)
