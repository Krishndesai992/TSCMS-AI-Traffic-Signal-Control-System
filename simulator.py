import pygame
import random

from simulation.vehicle import Vehicle
from simulation.road import draw_roads
from simulation.signal import SignalSystem
from ai.controller import TrafficController
from ai.emergency import EmergencyHandler

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)

class Simulator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI Traffic Signal Control System")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 22)

        self.vehicles = []
        self.signal_system = SignalSystem()
        self.controller = TrafficController(self.signal_system)
        self.emergency_handler = EmergencyHandler(self.signal_system)

        self.lane_names = ["NORTH", "EAST", "SOUTH", "WEST"]

    # 🚗 Controlled vehicle spawning (slower traffic)
    def spawn_vehicle(self):
        if random.randint(1, 50) == 1:  # 👈 realistic flow
            self.vehicles.append(Vehicle(random.randint(0, 3)))

    # 🚦 Draw signal lights
    def draw_signals(self):
        signals = self.signal_system.get_state()

        positions = [
            (CENTER + 110, CENTER - 140),  # NORTH
            (CENTER + 140, CENTER + 110),  # EAST
            (CENTER - 140, CENTER + 140),  # SOUTH
            (CENTER - 110, CENTER - 110)   # WEST
        ]

        for i in range(4):
            if signals[i] == "GREEN":
                color = GREEN
            elif signals[i] == "YELLOW":
                color = YELLOW
            else:
                color = RED

            pygame.draw.circle(self.screen, color, positions[i], 10)

    # 📊 Quadrant lane info
    def draw_lane_info(self, counts):
        positions = [
            (CENTER + 120, CENTER - 180),
            (CENTER + 180, CENTER + 120),
            (CENTER - 180, CENTER + 180),
            (CENTER - 200, CENTER - 180)
        ]

        for i in range(4):
            density = self.controller.get_density(counts[i])
            x, y = positions[i]

            self.screen.blit(self.font.render(self.lane_names[i], True, WHITE), (x, y))
            self.screen.blit(self.font.render(f"Vehicles: {counts[i]}", True, WHITE), (x, y + 20))
            self.screen.blit(self.font.render(f"Density: {density}", True, WHITE), (x, y + 40))

    # 🌍 Global system info
    def draw_global_info(self):
        current_lane = self.lane_names[self.signal_system.current_green]
        next_lane = self.lane_names[self.signal_system.next_lane]

        timer = self.signal_system.get_remaining_time()
        next_time = self.signal_system.next_green_time

        self.screen.blit(self.font.render(f"CURRENT: {current_lane}", True, WHITE), (10, 10))
        self.screen.blit(self.font.render(f"NEXT: {next_lane} ({next_time}s)", True, WHITE), (10, 30))
        self.screen.blit(self.font.render(f"TIMER: {timer}s", True, WHITE), (10, 50))

        # 🚑 Emergency info
        if self.emergency_handler.active or self.emergency_handler.emergency_mode:
            lane = self.lane_names[self.emergency_handler.emergency_lane]
            status = "ACTIVE" if self.emergency_handler.active else "CLEARING"
            self.screen.blit(
                self.font.render(f"EMERGENCY: {lane} ({status})", True, (255, 100, 100)),
                (10, 70)
            )

    # ▶ MAIN LOOP
    def run(self):
        running = True

        while running:
            dt = self.clock.tick(60) / 1000  # 👈 real seconds

            # 🧾 Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # 🚑 Detect emergency
            self.emergency_handler.detect_emergency(self.vehicles)

            # 🧠 Controller update (handles logic)
            counts = self.controller.update(
                self.vehicles,
                dt,
                self.emergency_handler
            )

            # 🚑 Handle buffer (post-emergency delay)
            self.emergency_handler.update_buffer(dt)

            # 🚗 Spawn vehicles
            self.spawn_vehicle()

            # 🎨 Draw environment
            draw_roads(self.screen)
            self.draw_signals()

            signals = self.signal_system.get_state()

            # 🚗 Move & draw vehicles
            for v in self.vehicles:
                v.move(signals[v.lane], self.vehicles)

                color = (255, 0, 0) if v.is_emergency else (0, 0, 255)
                pygame.draw.rect(self.screen, color, (v.x, v.y, v.width, v.height))

            # 📊 UI Info
            self.draw_lane_info(counts)
            self.draw_global_info()

            pygame.display.update()

        pygame.quit()