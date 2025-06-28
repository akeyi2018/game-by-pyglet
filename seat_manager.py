class SeatManager:
    def __init__(self, parent, customers):
        self.parent = parent
        self.customers = customers
        self.seat_positions = parent.map.seat_pos
        self.seat_occupied = [False] * len(self.seat_positions)
        # self.assigned_seats = {}
        # self.seated_customers = []
        # 各顧客の状態（moving_to_seat / seated など）を管理
        self.customer_states = ["idle"] * len(customers)
    
    def assign_seats(self):
        for i, customer in enumerate(self.customers):
            if self.customer_states[i] == "waiting":
                for j, (seat_x, seat_y) in enumerate(self.seat_positions):
                    if not self.seat_occupied[j]:
                        self.seat_occupied[j] = True
                        customer.set_new_target(seat_x, seat_y)
                        self.customer_states[i] = "moving_to_seat"
                        break

    def update(self, dt):
        for i, customer in enumerate(self.customers):
            state = self.customer_states[i]

            if state == "moving_to_seat":
                customer.update(dt, self.parent.map)

                if customer.reached_final_target:
                    self.customer_states[i] = "seated"

                    # Wの場所を空ける（waiting_queue は (cust_i, wait_i) タプルになっている前提）
                    for idx, (cust_i, wait_i) in enumerate(self.parent.customer_manager.waiting_queue):
                        if cust_i == i:
                            self.parent.customer_manager.wait_pos_in_use[wait_i] = False
                            self.parent.customer_manager.waiting_queue.pop(idx)
                            # print(f"[DEBUG] Customer {i} is now seated. Releasing wait_pos {wait_i}")
                            break

