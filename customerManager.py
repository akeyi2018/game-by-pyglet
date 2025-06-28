from settings import *
from customer import Customer

class CustomerManager:
    def __init__(self, parent, num_customers=2):
        self.parent = parent
        
        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch

        self.customer_pos_list = parent.map.get_random_customer_positions(num_customers)

        # Wの数だけしか wait_pos がない場合に備える
        self.wait_pos_list = parent.map.wait_pos
        self.waiting_queue = []  # Wに入った顧客のインデックス
        self.wait_pos_in_use = [False] * len(self.wait_pos_list)

        self.customer_states = []  # 各顧客の状態

        self.customers = []

        self.color = (0, 255, 255)
        # ⭐ wait_pos_list をループしても IndexError にならないよう保護
        for i in range(num_customers):
            start = self.customer_pos_list[i]
            wait = self.wait_pos_list[i] if i < len(self.wait_pos_list) else self.wait_pos_list[-1]  # 最後のWを使い回すなど

            customer = Customer(start, wait, self.window_height, self.cell_size, (0, 255, 255), self.batch)
            self.customers.append(customer)
            self.customer_states.append("outside")

        self.active_customer = self.customers[0] if self.customers else None
        # if self.active_customer:
        #     self.customer_states[0] = "moving_to_wait"
        
        # print(f"[DEBUG] CustomerManager: 顧客数 = {len(self.customers)}")

    def update(self, dt):
        # Step 1: W に空きがあれば、outside → moving_to_wait にする
        for i, state in enumerate(self.customer_states):
            if state == "outside":
                if i == 0:
                    print(f"[DEBUG] Checking if Customer {i} can be assigned to W")
                # すでに waiting_queue に入っているかチェック
                already_in_queue = any(cust_i == i for cust_i, _ in self.waiting_queue)
                if already_in_queue:
                    continue  # すでに追加済み → スキップ

                for j, used in enumerate(self.wait_pos_in_use):
                    if not used:
                        self.wait_pos_in_use[j] = True
                        self.waiting_queue.append((i,j))
                        customer = self.customers[i]
                        target = self.wait_pos_list[j]
                        customer.set_new_target(*target)
                        self.customer_states[i] = "moving_to_wait"
                        # print(f"[DEBUG] Customer {i} assigned to W[{j}]")
                        break  # 1人だけWに入れる

                
        # Step 2: moving_to_wait → waiting に状態変更
        for cust_i, wait_i in self.waiting_queue:
            customer = self.customers[cust_i]
            if self.customer_states[cust_i] == "moving_to_wait":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    self.customer_states[cust_i] = "waiting"
                    self.parent.seat_manager.customer_states[cust_i] = "waiting"
                    # print(f"[DEBUG] Customer {i} is now seated. Releasing wait_pos {wait_i}")

        # self.print_wait_pos_status()

    def print_wait_pos_status(self):
        status_line = "[WAIT_POS] "
        used_count = 0

        for i, used in enumerate(self.wait_pos_in_use):
            mark = "✓" if used else "×"
            status_line += f"{i}:{mark}  "
            if used:
                used_count += 1

        print(status_line)
        print(f"[W使用数] {used_count} / {len(self.wait_pos_in_use)}")
