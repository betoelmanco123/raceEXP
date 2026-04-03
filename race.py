import random, math

CONVERT = math.pi / 180

class RaceCar:
    
    def __init__(self, x=None, y=None, mapName="map.txt"):
        self.map = ReadMap(mapName)
        if x is None:
           self.position = getStart(self.map)
           self.x, self.y = self.position

        else:
            self.position = (x, y)
            self.x = x
            self.y = y
        self.speed = 1
        self.direccion = 90
        self.aceleration = .1
        self.goal = getGoal(self.map)
        self.turnSpeed = 12
        self.mutateSpeed = .1
        self.alive = True
        
        self.distanceTraveled = 0
        
        #Neurons
        self.w1 = random.uniform(-1, 1)
        self.w2 = random.uniform(-1, 1)
        self.w3 = random.uniform(-1, 1)
        self.w4 = random.uniform(-1, 1)

        #Raycast
        self.RayLarge = 10
        self.RayValues = None
        
    def think(self):
        
        rays = self.multipleRayCast()
        
        turn = self.w1 * rays[0] + self.w2 * rays[1] - self.w3 * rays[3] - self.w4 * rays[4]
        accel = rays[2]
        
        return (math.tanh(turn), math.tanh(accel))
        
    def acelerate(self):
        self.speed += self.aceleration
        
    def updatePosition(self, turn=0, accel=0):
        if not self.alive:
            return
        temp_x = self.x + self.speed * math.cos(self.direccion * (CONVERT))
        temp_y = self.y + self.speed * math.sin(self.direccion * (CONVERT))
        
        if temp_x > len(self.map[0]) or temp_x < 0:
            return False
        if temp_y > len(self.map) or temp_y < 0:
            return False
        
        if self.collition(temp_x, temp_y):
            self.alive = False
            return False
        self.direccion += turn
        self.speed += accel
        self.distanceTraveled += math.hypot(temp_x - self.x, temp_y- self.y)
        self.x = temp_x
        self.y = temp_y
        
        self.upToDate()
        
        return True
    
    def collition(self, x, y):
        y = math.floor(y)
        x = math.floor(x)
        if self.map[y][x] == "#":
            return (y, x)
        return False
    
    def upToDate(self):
        self.position = (self.x, self.y)
        

    def RayCast(self, angle):
        crash = None
        valueX = math.cos(math.radians(angle))
        valueY = math.sin(angle * CONVERT)
        for i in range(1, self.RayLarge + 1):

            rayX = i * valueX + self.x
            rayy = i * valueY + self.y
            if self.collition(rayX, rayy):
                crash = i
                by, bx = self.collition(rayX, rayy)
                break
        if crash:
            return getDistance((bx, by), self.position)
        return self.RayLarge + 1

    def haveChild(self):
        child = RaceCar()
        child.w1 = self.w1
        child.w2 = self.w2
        child.w3 = self.w3
        child.w4 = self.w4
        child.mutate()
        return child
    
    def mutate(self):
        self.w1 += random.uniform(-self.mutateSpeed , self.mutateSpeed)
        self.w2 += random.uniform(-self.mutateSpeed , self.mutateSpeed)
        self.w3 += random.uniform(-self.mutateSpeed , self.mutateSpeed)
        self.w4 += random.uniform(-self.mutateSpeed , self.mutateSpeed)
    
    def multipleRayCast(self):
        values = (
            self.RayCast(self.direccion - 90),
            self.RayCast(self.direccion - 45),
            self.RayCast(self.direccion),
            self.RayCast(self.direccion + 45),
            self.RayCast(self.direccion + 90),
            )
        self.RayValues = values
        return values
    
    def move(self):
        while True:
            self.updatePosition()
            self.printPosition()
        
    def printPosition(self):
        print(f"Car position({self.x}, {self.y})")
        print(f"Distance TRaveled {self.distanceTraveled}")
        print(f"raycast {self.RayCast(180)}")
            
    def printStats(self):
        print(f"Car position({self.x}, {self.y})")
        print(f"Distance TRaveled {self.distanceTraveled}")
        
        
    
    
class Map:
    
    def __init__(self, mapName):
        
        self.map = ReadMap(mapName)
        
    
    
def ReadMap(mapName):
    
    with open(mapName, "r",) as Map:
        
        valid_map = list()
        for line in Map:
            temp = list()
            for character in line:
                if character == "\n":
                    continue
                temp.append(character)
            valid_map.append(temp)
    return valid_map

def getStart(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == "S":
                return (j, i)
            
    return None

def getGoal(mapa):
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if mapa[i][j] == "G":
                return (j, i)
            
    return None

def getwinners(cars):
    values = dict()
    for car in cars:
        values[car] = car.distanceTraveled
    ordenado = sorted(values, key=values.get)
    
    return ordenado[-5:]

def getDistance(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    return math.hypot((ax - bx), (ay - by))


def play():
    everyone = [RaceCar() for _ in range(100)]

    for k in range(200):
        for m in range(200):
            for car in everyone:
                if not car.alive:
                    continue
                turn, accel = car.think()
                car.updatePosition(turn, accel)
        winners = getwinners(everyone)

        everyone = list()
        for fhater in winners:
            for _ in range(20):
                child = fhater.haveChild()
                everyone.append(child)
    for q in winners:
        q.printStats()

play()

