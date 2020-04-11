import numpy

class Map:
    def __init__(self):
        self.map = numpy.zeros((8, 8))
        self.map[0][2] = 1
        self.map[1][2] = 1
        self.map[1][3] = 1
        self.map[1][4] = 1
        self.map[1][5] = 1
        self.map[2][5] = 1
        self.map[3][5] = 1
        self.map[4][5] = 1
        self.map[5][5] = 1
        self.map[6][5] = 1
        self.map[7][5] = 1

    def buildTower(self, xCoord, yCoord):
        print("In buildTower")
        print("xCoord = ", xCoord)
        print("yCoord = ", yCoord)
        if(self.map[xCoord][yCoord] != 1):
            self.map[xCoord][yCoord] = 2

    def mobKilled(self, xCoord, yCoord):
        print("in mobKilled")
        self.map[xCoord][yCoord] = 1

    def getNextPathTile(self, xCoord, yCoord):
        if(xCoord == 0 and yCoord == 2):
            return (1,2)
        elif(xCoord == 1 and yCoord == 2):
            return (1,3)
        elif(xCoord == 1 and yCoord == 3):
            return (1,4)
        elif(xCoord == 1 and yCoord == 4):
            return (1,5)
        elif(xCoord == 1 and yCoord == 5):
            return (2,5)
        elif(xCoord == 2 and yCoord == 5):
            return (3,5)
        elif(xCoord == 3 and yCoord == 5):
            return (4,5)
        elif(xCoord == 4 and yCoord == 5):
            return (5,5)
        elif(xCoord == 5 and yCoord == 5):
            return (6,5)
        elif(xCoord == 6 and yCoord == 5):
            return (7,5)
        elif(xCoord == 7 and yCoord == 5):
            return (-1,-1)

    def moveMob(self, xCoord, yCoord):
        print("In moveMob")
        self.map[xCoord][yCoord] = 3

        # Change old coord to 1
        if(xCoord == 1 and yCoord == 2):
            self.map[0][2] = 1
        elif(xCoord == 1 and yCoord == 3):
            self.map[1][2] = 1
        elif(xCoord == 1 and yCoord == 4):
            self.map[1][3] = 1
        elif(xCoord == 1 and yCoord == 5):
            self.map[1][4] = 1
        elif(xCoord == 2 and yCoord == 5):
            self.map[1][5] = 1
        elif(xCoord == 3 and yCoord == 5):
            self.map[2][5] = 1
        elif(xCoord == 4 and yCoord == 5):
            self.map[3][5] = 1
        elif(xCoord == 5 and yCoord == 5):
            self.map[4][5] = 1
        elif(xCoord == 6 and yCoord == 5):
            self.map[5][5] = 1
        elif(xCoord == 7 and yCoord == 5):
            self.map[6][5] = 1


#theMap = Map().map
#print(theMap[0][0])