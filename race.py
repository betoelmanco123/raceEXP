import random, math
import processIm

CONVERT = math.pi / 180

validMap = processIm.get_matrix("sprites/map3.jpg")
startposition = (550, 50)




class RaceCar:

    def __init__(self, validMap=validMap, startposition=startposition):

        # car stats
        self.startposition = startposition
        self.position = startposition
        self.x, self.y = self.position
        self.speed = 3
        self.aceleration = 0.2
        self.mutateSpeed = 0.1
        self.turnSpeed = 1.8
        self.alive = True
        self.direction = 180
        self.distanceTraveled = 0
        self.hitbox = [13, 28]
        self.speedLimit = 5
        self.steering = 0
        self.length = 28
        self.known = set()
        self.reward = 0

        # map stats
        self.map = validMap
        self.checkpoints = [
            (100, 85),
            (100, 400),
            (100, 750),
            (450, 750),
            (750, 750),
            (820, 425),
            (800, 100),
        ]
        self.laps = 0
        self.counterCheckpoint = 0

        # Raycast
        self.RayLarge = 300
        self.RayValues = [0 for _ in range(5)]

        # Neurons
        self.hidden_size = 12
        self.input_size = 9
        self.output_size = 3
        self.angles = [-90, -45, 0, 45, 90]
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

    def updatePosition(self, steering=0, accel=0, time=0):
        if not self.alive:
            return
        self.speed += accel * time * 60
        self.speed = min(self.speedLimit, max(-self.speedLimit, self.speed))
        self.direction += steering * self.turnSpeed * (self.speed / self.speedLimit)
        self.direction %= 360
        rad = self.direction * (CONVERT)
        temp_x = self.x + self.speed * math.cos(rad)
        temp_y = self.y + self.speed * math.sin(rad)

        if temp_x >= len(self.map[0]) or temp_x < 0:
            self.alive = False
            return False
        if temp_y >= len(self.map) or temp_y < 0:
            self.alive = False
            return False

        if self.hitboxColittion(temp_x, temp_y):
            self.alive = False
            return False

        self.distanceTraveled += math.hypot(temp_x - self.x, temp_y - self.y)
        self.x = temp_x
        self.y = temp_y

        self.upToDate()

        if not self.position in self.known:
            self.known.add(self.position)
            self.reward += 1
        else:
            self.reward -= 1
        return True

    # AI
    def think(self, time):
        inputs = [v / self.RayLarge for v in self.multipleRayCast()]
        inputs.append(self.speed / self.speedLimit)
        inputs.append(math.sin(self.direction * CONVERT))
        inputs.append(math.cos(self.direction * CONVERT))
        inputs.append(time / 10)

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

        accel = outputs[0]
        right = outputs[1]
        left = outputs[2]

        turn = left - right
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
        if self._touch_checkpoint(x, y):
            return False

        if self.map[y][x] < 20:

            return (y, x)

        return False

    def hitboxColittion(self, x, y):
        y = math.floor(y)
        x = math.floor(x)

        if self._touch_checkpoint(x, y):
            return False

        heigh, width = self.hitbox

        heigh_half, width_half = heigh / 2, width / 2

        rectangle = [
            [(x - width_half, y - heigh_half), (x + width_half, y - heigh_half)],
            [(x - width_half, y + heigh_half), (x + width_half, y + heigh_half)],
        ]
        for face in rectangle:
            for point in face:
                sx, sy = point
                if self.isWall(sx, sy):
                    self.reward -= 100
                    return True
        return False

    def _touch_checkpoint(self, x, y):
        cx, cy = self.checkpoints[self.counterCheckpoint]

        if abs(x - cx) < 100 and abs(y - cy) < 100:
            self.counterCheckpoint += 1
            if self.counterCheckpoint >= len(self.checkpoints):
                self.counterCheckpoint = 0
                self.laps += 1
            return True

        return False

    # genetic mutation

    def haveChild(self):
        child = RaceCar()
        child.w_ih = [row[:] for row in self.w_ih]
        child.w_ho = [row[:] for row in self.w_ho]

        child.mutate()
            
        return child

    def mutate(self, speed=1):
        mutateSpeed = speed * self.mutateSpeed
        for row in self.w_ih:
            for j in range(len(row)):
                row[j] += random.uniform(-mutateSpeed, mutateSpeed)
        for row in self.w_ho:
            for j in range(len(row)):
                row[j] += random.uniform(-mutateSpeed, mutateSpeed)

    # ray cast
    def RayCast(self, angle):
        rad = angle * CONVERT
        valueX = math.cos(rad)
        valueY = math.sin(rad)
        for i in range(1, self.RayLarge + 1):

            rayX = i * valueX + self.x
            rayy = i * valueY + self.y
            coll = self.isWall(rayX, rayy)
            if coll:
                return i
        return self.RayLarge + 1

    def multipleRayCast(self):
        values = [
            self.RayCast(self.direction - 90),
            self.RayCast(self.direction - 45),
            self.RayCast(self.direction),
            self.RayCast(self.direction + 45),
            self.RayCast(self.direction + 90),
        ]
        self.RayValues = values
        return values

    # execute one turn
    def run(self, time):
        turn, accel = self.think(time)
        self.updatePosition(turn, accel, time)

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

    def print_laps(self):
        print(f"-------------------{self.laps}-----------")
        print(f"-------------------{self.counterCheckpoint}-----------")

    def goToStart(self):
        self.position = self.startposition
        self.x, self.y = self.position
        self.speed = 5
        self.distanceTraveled = 0
        self.alive = True
        self.counterCheckpoint = 0
        self.laps = 0
        self.known = set()
        self.reward = 0

    def get_genetics(self):
        genes = dict()

        genes["inputs"] = self.w_ih
        genes["outputs"] = self.w_ho

        return genes

    def upToDate(self):
        self.position = (self.x, self.y)


if __name__ == "__main__":
    print("Hello from race.py")
