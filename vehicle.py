import random
import math

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2

class Vehicle:
    def __init__(self, lane):
        self.lane = lane
        self.speed = 2

        self.crossed = False
        self.turn = random.choice(["straight", "left", "right"])
        self.turning = False
        self.angle = 0

        self.is_emergency = random.randint(1, 25) == 1

        lane_offset = random.choice([-40, -10])

        if lane == 0:
            self.x = CENTER + lane_offset
            self.y = 0
            self.dx = 0
            self.dy = self.speed

        elif lane == 1:
            self.x = WIDTH
            self.y = CENTER + lane_offset
            self.dx = -self.speed
            self.dy = 0

        elif lane == 2:
            self.x = CENTER - lane_offset
            self.y = HEIGHT
            self.dx = 0
            self.dy = -self.speed

        elif lane == 3:
            self.x = 0
            self.y = CENTER - lane_offset
            self.dx = self.speed
            self.dy = 0

        self.width = 20
        self.height = 40

    def move(self, signal_state, vehicles):
        stop_distance = 120
        junction_size = 70

        if self.lane == 0:
            stop_line = CENTER - stop_distance
        elif self.lane == 1:
            stop_line = CENTER + stop_distance
        elif self.lane == 2:
            stop_line = CENTER + stop_distance
        else:
            stop_line = CENTER - stop_distance

        if not self.crossed:
            if self.lane == 0 and self.y > stop_line:
                self.crossed = True
            elif self.lane == 1 and self.x < stop_line:
                self.crossed = True
            elif self.lane == 2 and self.y < stop_line:
                self.crossed = True
            elif self.lane == 3 and self.x > stop_line:
                self.crossed = True

        if not self.crossed:
            for v in vehicles:
                if v == self or v.lane != self.lane or v.crossed:
                    continue

                if self.lane == 0 and v.y > self.y and (v.y - self.y) < 50:
                    return
                elif self.lane == 1 and v.x < self.x and (self.x - v.x) < 50:
                    return
                elif self.lane == 2 and v.y < self.y and (self.y - v.y) < 50:
                    return
                elif self.lane == 3 and v.x > self.x and (v.x - self.x) < 50:
                    return

            if signal_state != "GREEN":
                if self.lane == 0 and self.y + self.height >= stop_line:
                    return
                elif self.lane == 1 and self.x <= stop_line:
                    return
                elif self.lane == 2 and self.y <= stop_line:
                    return
                elif self.lane == 3 and self.x + self.width >= stop_line:
                    return

        if not self.turning:
            if abs(self.x - CENTER) < junction_size and abs(self.y - CENTER) < junction_size:
                if self.turn != "straight":
                    self.turning = True

        if self.turning:
            turn_speed = 0.04
            self.angle += turn_speed if self.turn == "left" else -turn_speed

            if self.lane == 0:
                self.dx = self.speed * math.sin(self.angle)
                self.dy = self.speed * math.cos(self.angle)
            elif self.lane == 1:
                self.dx = -self.speed * math.cos(self.angle)
                self.dy = self.speed * math.sin(self.angle)
            elif self.lane == 2:
                self.dx = -self.speed * math.sin(self.angle)
                self.dy = -self.speed * math.cos(self.angle)
            elif self.lane == 3:
                self.dx = self.speed * math.cos(self.angle)
                self.dy = -self.speed * math.sin(self.angle)

            if abs(self.angle) >= math.pi / 2:
                self.turning = False
                self.angle = 0

        self.x += self.dx
        self.y += self.dy