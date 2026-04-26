class SignalSystem:
    def __init__(self):
        self.signals = ["GREEN", "RED", "RED", "RED"]
        self.current_green = 0
        self.next_lane = 1

        self.timer = 0
        self.green_duration = 10
        self.yellow_duration = 3

        self.state = "GREEN"
        self.next_green_time = 10

    def set_green(self, lane, next_time=10):
        self.current_green = lane
        self.next_lane = (lane + 1) % 4

        self.next_green_time = next_time

        self.state = "GREEN"
        self.timer = 0

        for i in range(4):
            self.signals[i] = "GREEN" if i == lane else "RED"

    def set_yellow(self):
        self.state = "YELLOW"
        self.timer = 0

        for i in range(4):
            self.signals[i] = "YELLOW" if i == self.current_green else "RED"

    def update_timer(self, dt):
        self.timer += dt

    def get_remaining_time(self):
        if self.state == "GREEN":
            return max(0, int(self.green_duration - self.timer))
        return max(0, int(self.yellow_duration - self.timer))

    def get_state(self):
        return self.signals