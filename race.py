import random, math
import processIm

CONVERT = math.pi / 180

validMap = processIm.get_matrix("sprites/map0.jpg")
startposition = (400, 150)

class RaceCar:

    def __init__(self, validMap=validMap, startposition=startposition):

            
        # car stats
        self.position = startposition
        self.x, self.y = self.position
        self.speed = 1
        self.aceleration = 0.1
        self.mutateSpeed = 0.1
        self.turnSpeed = 12
        self.alive = True
        self.direccion = 180
        self.distanceTraveled = 0
        
        # map stats
        self.map = validMap
        self.checkpoints = [(390, 150), (375, 150), (150, 450), (375, 720), (150, 450)]
        self.laps = 0
        self.counterCheckpoint = 0


        # Raycast
        self.RayLarge = 50
        self.RayValues = None
        
        
        # Neurons
        self.hidden_size = 4
        self.input_size = 6
        self.output_size = 2
        self.w_ih = [
            [random.uniform(-1, 1) for _ in range(self.input_size)]
            for _ in range(self.hidden_size)
        ]
        self.w_ho = [
            [random.uniform(-1, 1) for _ in range(self.hidden_size)]
            for _ in range(self.output_size)
        ]

        

    # Control of the car
    def acelerate(self):
        self.speed += self.aceleration

    def updatePosition(self, turn=0, accel=0):
        if not self.alive:
            return
        speed = self.speed + accel
        direccion = self.direccion + turn
        rad = direccion * (CONVERT)
        temp_x = self.x + speed * math.cos(rad)
        temp_y = self.y + speed * math.sin(rad)

        if temp_x >= len(self.map[0]) or temp_x < 0:
            return False
        if temp_y >= len(self.map) or temp_y < 0:
            return False

        if self.collition(temp_x, temp_y):
            self.alive = False
            return False
        self.direccion = direccion % 360
        self.speed = max(0, speed)
        self.distanceTraveled += math.hypot(temp_x - self.x, temp_y - self.y)
        self.x = temp_x
        self.y = temp_y

        self.upToDate()

        return True

    # AI
    def think(self):

        inputs = [v / self.RayLarge for v in self.multipleRayCast()]
        inputs.append(self.speed / 10)

        hidden = []
        for i in range(self.hidden_size):
            suma = 0
            for j in range(self.input_size):
                suma += self.w_ih[i][j] * inputs[j]

            hidden.append(math.tanh(suma))
        outputs = []
        for i in range(self.output_size):
            suma = 0
            for j in range(self.hidden_size):
                suma += self.w_ho[i][j] * hidden[j]

            outputs.append(math.tanh(suma))

        turn = outputs[0]
        accel = outputs[1]

        return turn, accel

    # map
    def isWall(self, x, y):
        y = math.floor(y)
        x = math.floor(x)

        if y >= len(self.map) or y < 0:
            return True
        if x >= len(self.map[0]) or x < 0:
            return True

        return self.map[y][x] < 20

    def collition(self, x, y):
        y = math.floor(y)
        x = math.floor(x)

        if y >= len(self.map):
            y = len(self.map) - 1

        if x >= len(self.map[0]):
            x = len(self.map[0]) - 1

        if y < 0:
            y = 0
        if x < 0:
            x = 0
        cx, cy = self.checkpoints[self.counterCheckpoint]

        if abs(x - cx) < 30 and abs(y - cy) < 30:
            self.counterCheckpoint += 1
            if self.counterCheckpoint >= len(self.checkpoints):
                self.counterCheckpoint = 0
            return False

        if self.map[y][x] < 20:

            return (y, x)

        return False

    # genetic mutation

    def haveChild(self):
        child = RaceCar()
        child.w_ih = [row[:] for row in self.w_ih]
        child.w_ho = [row[:] for row in self.w_ho]
        child.mutate()
        return child

    def mutate(self):

        for row in self.w_ih:
            for j in range(len(row)):
                row[j] += random.uniform(-self.mutateSpeed, self.mutateSpeed)
        for row in self.w_ho:
            for j in range(len(row)):
                row[j] += random.uniform(-self.mutateSpeed, self.mutateSpeed)

    # ray cast
    def RayCast(self, angle):
        crash = None
        valueX = math.cos(math.radians(angle))
        valueY = math.sin(angle * CONVERT)
        for i in range(1, self.RayLarge + 1):

            rayX = i * valueX + self.x
            rayy = i * valueY + self.y
            coll = self.isWall(rayX, rayy)
            if coll:
                crash = i
                by, bx = rayy, rayX
                break
        if crash:
            return getDistance((bx, by), self.position)
        return self.RayLarge + 1

    def multipleRayCast(self):
        values = [
            self.RayCast(self.direccion - 90),
            self.RayCast(self.direccion - 45),
            self.RayCast(self.direccion),
            self.RayCast(self.direccion + 45),
            self.RayCast(self.direccion + 90),
        ]
        self.RayValues = values
        return values
    
    # execute one turn
    def run(self):
        turn, accel = self.think()
        self.updatePosition(turn, accel)
        self.speed *= 0.98

    # auxiliar
    def printPosition(self):
        print(f"Car position({self.x}, {self.y})")
        print(f"Distance TRaveled {self.distanceTraveled}")
        print(f"raycast {self.RayCast(180)}")

    def printStats(self):
        print(f"Car position({self.x}, {self.y})")
        print(f"Distance TRaveled {self.distanceTraveled}")
        print(f"the speed is {self.speed}")
        print(f"this car achived {self.laps} laps")

    def upToDate(self):
        self.position = (self.x, self.y)


def ReadMap(mapName):

    with open(
        mapName,
        "r",
    ) as Map:

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
        values[car] = 10 * (car.laps * 4 + car.counterCheckpoint)
    ordenado = sorted(values, key=values.get)

    return ordenado[-5:]


def getDistance(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    return math.hypot((ax - bx), (ay - by))


def play():
    everyone = [RaceCar() for _ in range(100)]

    for k in range(100):
        for m in range(200):
            for car in everyone:
                if not car.alive:
                    continue
                car.run()
        winners = getwinners(everyone)

        everyone = list()
        for fhater in winners:
            for _ in range(20):
                child = fhater.haveChild()
                everyone.append(child)
    for q in winners:
        q.printStats()


if __name__ == "__main__":
    play()
