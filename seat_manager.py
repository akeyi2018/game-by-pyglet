class SeatManager:
    def __init__(self, parent):
        self.parent = parent
        self.seat_positions = parent.map.seat_pos
        self.assigned_seats = {}
        self.seated_customers = []

    def update(self, dt):
        waiting_customers = self.parent.customer_manager.get_waiting_customers()

        for customer in waiting_customers:
            if customer in self.seated_customers:
                continue

            if customer not in self.assigned_seats:
                for seat in self.seat_positions:
                    if seat not in self.assigned_seats.values():
                        self.assigned_seats[customer] = seat
                        customer.start_moving_to(*seat)
                        print("→ 座席へ移動開始:", seat)
                        break
            else:
                customer.update(dt, self.parent.map)
                seat_x, seat_y = self.assigned_seats[customer]
                if not customer.moving and customer.is_at_position(seat_x, seat_y):
                    self.seated_customers.append(customer)
                    print("✅ 着席完了:", (seat_x, seat_y))

