MIN_GREEN = 10
MAX_GREEN = 30

class TrafficController:
    def __init__(self, signal_system):
        self.signal_system = signal_system

        self.last_lane = 0
        self.interrupted_lane = None  # 👈 NEW

    def count_vehicles(self, vehicles):
        counts = [0, 0, 0, 0]
        for v in vehicles:
            if not v.crossed:
                counts[v.lane] += 1
        return counts

    def get_density(self, count):
        if count < 5:
            return "LOW"
        elif count < 10:
            return "MEDIUM"
        else:
            return "HIGH"

    def update(self, vehicles, dt, emergency_handler):
        counts = self.count_vehicles(vehicles)
        lane = self.signal_system.current_green

        # lock green time
        if self.signal_system.timer == 0:
            green_time = min(MIN_GREEN + counts[lane]*2, MAX_GREEN)
            self.signal_system.green_duration = green_time

        self.signal_system.update_timer(dt)

        # ---------------- GREEN ----------------
        if self.signal_system.state == "GREEN":
            if self.signal_system.timer >= self.signal_system.green_duration:
                self.signal_system.set_yellow()

        # ---------------- YELLOW ----------------
        elif self.signal_system.state == "YELLOW":
            if self.signal_system.timer >= self.signal_system.yellow_duration:

                # 🚑 START EMERGENCY MODE
                if emergency_handler.active and not emergency_handler.emergency_mode:
                    self.interrupted_lane = (lane + 1) % 4
                    emergency_handler.start_emergency()

                    next_lane = emergency_handler.emergency_lane

                # 🚑 CONTINUE EMERGENCY MODE
                elif emergency_handler.emergency_mode:
                    next_lane = emergency_handler.emergency_lane

                # 🔁 RESUME AFTER EMERGENCY
                elif self.interrupted_lane is not None:
                    next_lane = self.interrupted_lane
                    self.interrupted_lane = None

                # 🔁 NORMAL ROUND ROBIN
                else:
                    next_lane = (self.last_lane + 1) % 4

                next_time = min(MIN_GREEN + counts[next_lane]*2, MAX_GREEN)

                self.signal_system.set_green(next_lane, next_time)
                self.last_lane = next_lane

        return counts