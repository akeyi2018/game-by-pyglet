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

        # self.shift_waiting_customers_forward()

        self.eating(dt)

        self.move_to_exit(dt)

    def assign_seat(self):
        for customer, wait_idx in self.parent.customer_manager.waiting_queue:
            if customer.state == "waiting":
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        customer.set_new_target(*self.parent.map.seat_pos[j])
                        customer.state = "moving_to_seat"
                        customer.sprite.color = (231,115,35)
                        self.seat_queue.append((customer, j))
                        self.log(f"【座席割当】id: {customer.id} → seat[{j}]")
                        # Wを解放し、詰め処理へ
                        self.parent.customer_manager.wait_pos_in_use[wait_idx] = False
                        self.parent.customer_manager.waiting_queue.remove((customer, wait_idx))
                        self.parent.customer_manager.shift_waiting_customers_forward()
                        return

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

