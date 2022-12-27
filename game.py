PLAYER = 'P'
SPACE  = '.'
WALL = '#'
TRAP = "X"
GOAL = "G"

DOWN = "down"
LEFT = "left"
RIGHT = "right"
UP = "up"

ACTIONS = [DOWN,LEFT,RIGHT,UP]

class Game:
    def __init__(self,filePath):
        """
        Assumes a txt file at `filePath` that is structured like this:\n
        5 6 \n
        ##### \n
        #...# \n
        #.XG# \n
        P..C# \n
        #...# \n
        ##### \n

        Where the first line contains 2 numbers that represent the width and height of the grid.

        \# = Wall \n
        . = Open Space \n
        P = Player \n
        F = GOAL position \n
        X = Trap \n


        """
        self.map = []
        f = open(filePath, "r")
        self.score = 0
        self.finished = False
        for index,line in enumerate(f.readlines()):
            if(index == 0):
                sizes = line.split(" ")
                self.width = int(sizes[0])
                self.height = int(sizes[1])
            else:
                row = []
                for i in range(self.width):
                    character = line[i]

                    if character == PLAYER:
                        row.append(SPACE)
                        self.start_position = {
                            "x": i,
                            "y": index - 1
                        }
                        self.player = {
                            "x": i,
                            "y": index - 1
                        }
                    else:
                        row.append(character)
                self.map.append(row)

    def execute(self,action):
        """Executes the `action` provided. Every action that gets taken `self.score` gets subtracted by 1"""
        px = self.player["x"]
        py = self.player["y"]

        if(action == "up"):
            if(py != 0 and self.map[py - 1][px] != WALL):
                self.player["y"] -= 1
        elif(action == "down"):
            if(py != self.height - 1 and self.map[py + 1][px] != WALL):
                self.player["y"] += 1
        elif(action == "left"):
            if(px != 0 and self.map[py][px - 1] != WALL):
                self.player["x"] -= 1
        elif(action == "right"):
            if(px != self.width - 1 and self.map[py][px + 1] != WALL):
                self.player["x"] += 1
        
        if self.isPlayerOnTrap():
            self.score -= 100
            # self.finished = True
            self.player["y"] = self.start_position["y"]
            self.player["x"] = self.start_position["x"]
            return -100

        if self.isPlayerOnGOAL():
            self.finished = True
            return 0
        self.score -= 1
        return -1
     
    def isPlayerOnTrap(self):
        """Returns `True` if the player is currently on a trap"""
        if self.map[self.player["y"]][self.player["x"]] == TRAP:
            return True

    def isPlayerOnGOAL(self):
        """Returns `True` if the player is currently on a GOAL"""
        if self.map[self.player["y"]][self.player["x"]] == GOAL:
            return True
