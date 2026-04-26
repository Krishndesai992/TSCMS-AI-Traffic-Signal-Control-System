class EmergencyHandler:
    def __init__(self, signal_system):
        self.signal_system = signal_system
        self.active = False
        self.emergency_lane = None

        self.emergency_mode = False
        self.buffer_time = 3
        self.buffer_timer = 0

    def detect_emergency(self, vehicles):
        for v in vehicles:
            if v.is_emergency and not v.crossed:
                self.active = True
                self.emergency_lane = v.lane
                return True

        self.active = False
        return False

    def start_emergency(self):
        self.emergency_mode = True
        self.buffer_timer = 0

    def update_buffer(self, dt):
        if not self.active and self.emergency_mode:
            self.buffer_timer += dt

            if self.buffer_timer >= self.buffer_time:
                self.emergency_mode = False
                return True  # 👈 emergency finished

        return False