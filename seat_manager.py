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

        # 顧客リスト（CustomerManagerを参照)
        self.customers = self.parent.customer_manager.customers
        # print(self.customers)
    
    def update(self, dt):

        self.assign_seat()

        self.move_to_seat(dt)

        self.eating(dt)

        self.move_to_exit(dt)

    def assign_seat(self):

        # 👇 座席が空いていれば waiting 状態の顧客を座席に誘導
        for customer in self.customers:
            if customer.state == "waiting":
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        seat_pos = self.parent.map.seat_pos[j]
                        customer.set_new_target(*seat_pos)
                        # 顧客をキューへ
                        self.seat_queue.append((customer, j)) 

                        customer.state = "moving_to_seat"
                        self.log(f"【座席割当】id: {customer.id} seat: [{j}] pos: {seat_pos} state:{customer.state}")
                        break  # この顧客には席が見つかったので、次の顧客へ

    def move_to_seat(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_seat":
                # 待機場所は解放する
                for idx, (cust_obj, wait_i) in enumerate(self.parent.customer_manager.waiting_queue):
                    if cust_obj == customer:
                        self.parent.customer_manager.wait_pos_in_use[wait_i] = False
                        self.parent.customer_manager.waiting_queue.pop(idx)
                        self.log(f"【席移動開始】id: {customer.id} W[ {wait_i} ] state: {customer.state}")

                customer.update(dt, self.parent.map)
                if customer.reached_final_target:
                    customer.state = "seated"
                    self.log(f"【着座】id: {customer.id} state: {customer.state}")

    def eating(self, dt):
        for customer in self.customers:
            if customer.state == "seated":
                customer.stay_timer += dt
                if customer.stay_timer >= STAY_DURATION:
                    # 退店へ
                    exit_x, exit_y = self.parent.map.exit_pos_list[0]  # 複数あるならランダムでもOK
                    customer.set_new_target(exit_x, exit_y)
                    customer.state = "leaving"
                    customer.sprite.color = (255,0,0)
                    self.log(f"【出口移動開始】id: {customer.id} Exit pos: {exit_x, exit_y} state: {customer.state}")  

                    # ✅ 座席の解放
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == customer:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
                            self.log(f"【座席解放】id: {customer.id} seat: [{seat_i}]")  

    def move_to_exit(self, dt):
        for customer in self.customers:
            if customer.state == "leaving":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "exited"
                    self.log(f"【退店】id: {customer.id} state: {customer.state}")
