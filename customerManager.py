from settings import *
from customer import Customer

class CustomerManager:
    def __init__(self, parent):
        self.parent = parent
        self.customer_pos_list = parent.map.customer_pos
        self.wait_pos_list = parent.map.wait_pos
        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height

        self.customers = []
        self.current_index = 0
        self.batch = self.parent.batch

        for i, (start, target) in enumerate(zip(self.customer_pos_list, self.wait_pos_list)):
            # color = (255, 0, 0) if i % 2 == 0 else (0, 128, 255)
            color = (0, 255, 255)
            customer = Customer(start, target, 
                                self.window_height, 
                                self.cell_size,
                                color, 
                                self.batch)
            self.customers.append(customer)

        self.active_customer = self.customers[0] if self.customers else None

    def update(self, dt):
        if not self.active_customer:
            return

        self.active_customer.update(dt, self.parent.map)

        if self.active_customer.reached_target:
            self.current_index += 1
            if self.current_index < len(self.customers):
                self.active_customer = self.customers[self.current_index]
            else:
                self.active_customer = None  # 全員移動完了

