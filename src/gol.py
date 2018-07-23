""" Simple ascii-based game of life ; by weld, wtfpl
"""

"""Conway's game of life rules: 
    - Any live cell with fewer than two live neighbours dies, as if caused by underpopulation. 
    - Any live cell with two or three live neighbours lives on to the next generation.
    - Any live cell with more than three live neighbours dies, as if by overpopulation.
    - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""
### === IMPORT === ###
try:
    from random import choice
    from copy import deepcopy
    from time import sleep
    from os import system
    
    import argparse as argp
except ImportError as err:
    print("[ERROR] ImportError : ", err)
### === CONST === ###
### === CLASS === ###
class Cell:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        self.alive = False

class Grid:
    def __init__(self, path, speed=None):
        self._filepath = path 
        self._rows = None
        self._columns = None
        self._matrix = []
        self._step = 0
        self._speed = speed
        self._ttlAlive = 0

        self._possibleChar = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+!=$€£")

    def _next_state(self):
        temp = deepcopy(self._matrix)
        for i in range(self._rows):
            for j in range(self._columns):
                n = self._count_alive_neigh(temp[i][j], temp)
                if n == 3:
                    self._matrix[i][j].alive = True
                elif n < 2 or n > 3:
                    self._matrix[i][j].alive = False
    
    def _draw(self):
        self._ttlAlive = 0
        for i in range(self._rows):
            for j in range(self._columns):
                if self._matrix[i][j].alive == True:
                    self._ttlAlive += 1
                    char = choice(self._possibleChar)
                    print(char, end='')
                else:
                    print(" ", end='')
            print("") # == \n
        print("========== STEP : %i | Living cells : %i ==========" % (self._step, self._ttlAlive))
        self._step += 1

    def _coord_in_bounds(self, neigh):
	    (c_x,c_y) = neigh
	    return(c_x >= 0 and c_x < self._rows and c_y >= 0 and c_y < self._columns)

    def _count_alive_neigh(self, c, matrix):
        # Simply counts the number of alive neighbors 
        """ x x x (X-1, Y-1) (X-1, Y) (X-1, Y+1)
            x x x (X, Y-1)   (X, Y)   (X, Y+1)
            x x x (X+1, Y-1) (X+1, Y) (X+1, Y+1)
        """
        count = 0
        neigh = [
            (c.x-1, c.y-1), (c.x-1, c.y), (c.x-1, c.y+1),
            (c.x, c.y-1),                 (c.x, c.y+1),
            (c.x+1, c.y-1), (c.x+1, c.y), (c.x+1, c.y+1)
        ]
        for i in neigh:
            if self._coord_in_bounds(i):
                if matrix[i[0]][i[1]].alive:
                    count += 1
        return count
    
    def _gen_matrix(self):
        FILE = open(self._filepath, 'r')
        for i, l in enumerate(FILE):
            self._matrix.append([])
            for j, w in enumerate(l[:-1].split()):
                c = Cell((i, j))
                print(w)
                if int(w) == 1:
                    c.alive = True
                self._matrix[i].append(c)
        FILE.close()

    def generate(self, size):
        FILE = open(self._filepath, 'w')
        for i in range(size[0]):
            for j in range(size[1]):
                FILE.write("0 ")
            FILE.write("\n")
        FILE.close()

    def run(self):
        # generate a matrix
        self._gen_matrix()

        # set size
        self._rows = len(self._matrix)-1
        self._columns = len(self._matrix[0])-1

        # init
        self._step = 0

        # main loop
        while True:
            system("clear")
            self._draw()
            self._next_state()
            sleep(self._speed)

### === FUNCTIONS === ###
### === ENTRY POINT === ###
if __name__=='__main__':
    try:
        parser = argp.ArgumentParser(description="A simple Conway's game of life written in python")
        parser.add_argument('path', nargs='?', help="path to the matrix file")
        parser.add_argument('-s', '--speed', type=float, default=(1/3), help="change the speedrate of the screen refresh")
        parser.add_argument('-m', '--matrix', metavar=("ROWS", "COLS"), nargs=2, type=int, help="generate a file with a given size")
        
        r = vars(parser.parse_args())
        if r['path']:
            Grid(r['path'], r['speed']).run()
        elif r['matrix']:
            Grid('new_matrix.txt').generate((r['matrix'][0], r['matrix'][1]))
        else:
            parser.print_help()
       
    except argp.ArgumentError as err:
        print("[ERROR] ArgumentError : ", err)
