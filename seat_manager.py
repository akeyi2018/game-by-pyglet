from settings import *

class SeatManager:

    def __init__(self, parent, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None

        # MAP上の座席の座標リスト
        self.seat_positions = parent.map.seat_pos
        # 座席管理リスト(使われているかどうか)
        self.seat_in_use = [False] * len(self.seat_positions)
        # 座席キュー（顧客と座席の紐づけ）
        self.seat_queue = []

        self.customers = []          # 顧客リスト（Customerオブジェクト）
        self.customer_states = []    # 顧客の状態文字列
        
    def set_customer_list(self, customer_list, state_list):
        self.customers = customer_list
        self.customer_states = state_list
    
    def update(self, dt):

        self.assign_seat()

        self.move_to_seat(dt)

        self.eating(dt)

        self.move_to_exit(dt)

    def assign_seat(self):

        # 👇 座席が空いていれば waiting 状態の顧客を座席に誘導
        for i, state in enumerate(self.customer_states):
            if state == "waiting":
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        seat_pos = self.parent.map.seat_pos[j]
                        customer = self.customers[i]
                        customer.set_new_target(*seat_pos)
                        # 顧客をキューへ
                        self.seat_queue.append((customer, j)) 

                        self.customer_states[i] = "moving_to_seat"
                        self.log(f"【座席割当】id: {customer.id} seat: [{j}] pos: {seat_pos}")
                        break  # この顧客には席が見つかったので、次の顧客へ

    def move_to_seat(self, dt):
        for i, customer in enumerate(self.customers):
            state = self.customer_states[i]
            if state == "moving_to_seat":
                # 待機場所は解放する
                for idx, (cust_obj, wait_i) in enumerate(self.parent.customer_manager.waiting_queue):
                    if cust_obj == customer:
                        self.parent.customer_manager.wait_pos_in_use[wait_i] = False
                        self.parent.customer_manager.waiting_queue.pop(idx)
                        self.log(f"【席移動開始】id: {customer.id} W[ {wait_i} ] state: {state}")

                customer.update(dt, self.parent.map)
                if customer.reached_final_target:
                    self.customer_states[i] = "seated"
                    self.log(f"【着座】id: {customer.id} state: {self.customer_states[i]}")

    def eating(self, dt):
        for i, customer in enumerate(self.customers):
            state = self.customer_states[i]
            if state == "seated":
                customer.stay_timer += dt
                if customer.stay_timer >= STAY_DURATION:
                    # 退店へ
                    exit_x, exit_y = self.parent.map.exit_pos_list[0]  # 複数あるならランダムでもOK
                    customer.set_new_target(exit_x, exit_y)
                    self.customer_states[i] = "leaving"
                    self.log(f"【出口移動開始】id: {customer.id} Exit pos: {exit_x, exit_y} state: {self.customer_states[i]}")  

                    # ✅ 座席の解放
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == customer:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
                            self.log(f"【座席解放】id: {customer.id} seat: [{seat_i}]")  

            # elif state == "leaving":
            #     customer.update(dt, self.parent.map)
            #     if not customer.is_moving and customer.reached_final_target:
            #         customer.marked_for_removal = True
            #         self.customer_states[i] = "exited"
            #         self.parent.customer_manager.customer_states[i] = "exited"
            #         self.log(f"【退店】id: {customer.id} state: {self.customer_states[i]}")
    
    def move_to_exit(self, dt):
        for i, customer in enumerate(self.customers):
            state = self.customer_states[i]
            if state == "leaving":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.marked_for_removal = True
                    self.customer_states[i] = "exited"
                    self.parent.customer_manager.customer_states[i] = "exited"
                    self.log(f"【退店】id: {customer.id} state: {self.customer_states[i]}")
