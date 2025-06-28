from settings import *
from customer import Customer

class CustomerManager:
    def __init__(self, parent):
        self.parent = parent
        self.customer_pos_list = parent.map.customer_pos
        self.wait_pos_list = parent.map.wait_pos
        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.customer_states = []  # 各顧客の状態

        self.customers = []
        self.current_index = 0
        self.batch = self.parent.batch

        for i, (start, target) in enumerate(zip(self.customer_pos_list, self.wait_pos_list)):
            color = (0, 255, 255)
            customer = Customer(start, target, 
                                self.window_height, 
                                self.cell_size,
                                color, 
                                self.batch)
            self.customers.append(customer)
            self.customer_states.append("waiting")

        self.active_customer = self.customers[0] if self.customers else None
        if self.active_customer:
            self.customer_states[0] = "moving"

    def update(self, dt):
        if not self.active_customer:
            return

        index = self.current_index
        customer = self.active_customer
        state = self.customer_states[index]

        if state == "moving": 

            customer.update(dt, self.parent.map)

            if not customer.is_moving and customer.reached_final_target:

                # 到着したと判断して状態を変更
                self.customer_states[index] = "arrived"  # or "arrived"

                # 次の顧客をアクティブに
                self.current_index += 1
                if self.current_index < len(self.customers):
                    self.active_customer = self.customers[self.current_index]
                    self.customer_states[self.current_index] = "moving"
                else:
                    self.active_customer = None  # 全員移動完了
