PLAYER = 'P'
SPACE  = '.'
WALL = '#'
COIN = "C"
TRAP = "X"
GOAL = "G"

DOWN = "down"
LEFT = "left"
RIGHT = "right"
UP = "up"

ACTIONS = [DOWN,LEFT,RIGHT,UP]

class Game:
    def __init__(self,filePath, version = 0):
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
        C = Coin \n
        F = GOAL position \n
        X = Trap \n

        If `version = 0` no coins will be loaded.
        If `version = 1` no traps will be loaded.
        If `version = 2` Everything will be loaded.

        """
        self.map = []
        f = open(filePath, "r")
        self.version = version
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

                    if self.version < 2 and character == TRAP:
                        character = SPACE

                    if self.version < 1 and character == COIN:
                        character = SPACE
                    
                    if character == PLAYER:
                        row.append(SPACE)
                        self.player = {
                            "x": i,
                            "y": index - 1
                        }
                    else:
                        row.append(character)
                self.map.append(row)

    def printState(self):
        """
            Pretty prints the current state of the map including the position of the players.
        """
        for y in range(self.height):
            for x in range(self.width):
                if y == self.player['y'] and x == self.player['x']:
                    print("P", end="")
                else:
                    print(self.map[y][x], end="")
            print()
        print()

    def execute(self,action):
        """Executes the `action` provided. Every action that gets taken `self.score` gets subtracted by 1"""
        px = self.player["x"]
        py = self.player["y"]
        self.score -= 1
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
        
        if self.isPlayerOnCoin():
            self.score += 1000
            self.map[self.player['x']][self.player['y']] = SPACE
            return 10

        if self.isPlayerOnTrap():
            self.finished = True
            return -100

        if self.isPlayerOnGOAL():
            self.score += 10000
            self.finished = True
            return 100
        return 0
     
    def isPlayerOnCoin(self):
        """Returns `True` if the player is currently on a coin"""
        if self.map[self.player["y"]][self.player["x"]] == COIN:
            return True

    def isPlayerOnTrap(self):
        """Returns `True` if the player is currently on a trap"""
        if self.map[self.player["y"]][self.player["x"]] == TRAP:
            return True

    def isPlayerOnGOAL(self):
        """Returns `True` if the player is currently on a GOAL"""
        if self.map[self.player["y"]][self.player["x"]] == GOAL:
            return True
           
    def play(self, algo = None):
        """ 
            Plays the game and returns the score if the game is in a finished state or if the
            player has no availble actions. 

            If `algo` is provided then that function is used to decide what action to take. \n
            Otherwise the user is provided with a promt the choose an action. \n
            The algo function should have the following parameters: \n
            `map`, `player`, `score`, `is_finished`
        """
        if algo == None:
            self.printState()

        while(self.finished == False):
            action = ""
            if algo:
                action = algo(self.map,self.player,self.score, self.finished)
            else:
                action = input("Choose an action: ")
            if not action in ACTIONS:
                print(f"{action} is not a valid action!")
            else:
                self.execute(action)
            
            if algo == None:
                self.printState()
            
            if(len(self.getAvailableActions()) == 0):
                break
        return self.score
    

    def getAvailableActions(self):
        """
        Returns all available actions that are available to player in its current state
        """
        px = self.player["x"]
        py = self.player["y"]
        actions = []
        if(py != 0 and self.map[py - 1][px] != WALL):
            actions.append("up")
        elif(py != self.height - 1 and self.map[py + 1][px] != WALL):
            actions.append("down")
        elif(px != 0 and self.map[py][px - 1] != WALL):
            actions.append("left")
        elif(px != self.width - 1 and self.map[py][px + 1] != WALL):
            actions.append("right")
        return actions

if __name__ == '__main__':
    game = Game("./map.txt", version=2)
    game.play()