from settings import *

# 座席管理クラス
class SeatManager:

    def __init__(self, parent, log_func=None):

        # parentはMainGameクラスのインスタンスを想定
        self.parent = parent
        # ログ関数が渡されていない場合は、何もしない関数をデフォルトに設定
        self.log = log_func if log_func else lambda msg: None

        # MAP上の座席の座標リスト
        self.seat_positions = parent.map.seat_pos
        # 座席管理リスト(使われているかどうか)
        self.seat_in_use = [False] * len(self.seat_positions)
        # 座席キュー（顧客と座席の紐づけ）
        self.seat_queue = []

        # 顧客リスト（CustomerManagerを参照)
        self.customers = self.parent.customer_manager.customers
    
    # 座席の割当、移動、飲食時間のカウント、退店処理を行うupdate関数
    def update(self, dt):

        # 座席の割当
        self.assign_seat()

        # 座席に移動中の顧客を更新
        self.move_to_seat(dt)
        
        # 着席中の顧客の飲食時間をカウントし、一定時間経過したら退店へ移行
        self.eating(dt)

        # 退店処理
        self.move_to_exit(dt)

        # 混雑度ラベルの更新
        self.update_crowd_label()

    # 待機中の顧客に空いている座席を割り当てる関数
    def assign_seat(self):
        for customer, wait_idx in self.parent.customer_manager.waiting_queue:
            if customer.state == "waiting":
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        customer.set_new_target(*self.parent.map.seat_pos[j])
                        customer.state = "moving_to_seat"
                        # customer.sprite.color = (231,115,35)
                        self.seat_queue.append((customer, j))
                        self.log(f"【座席割当】id: {customer.id} → seat[{j}]")

                        if j%2 == 0:
                            customer.face_direction = 'right'
                        else:
                            customer.face_direction = 'left'
                        # Wを解放し、詰め処理へ
                        self.parent.customer_manager.wait_pos_in_use[wait_idx] = False
                        self.parent.customer_manager.waiting_queue.remove((customer, wait_idx))
                        self.parent.customer_manager.shift_waiting_customers_forward()
                        return
                    
    # 顧客を座席に移動させる関数
    def move_to_seat(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_seat":
                self.log(f"【席移動開始】id: {customer.id} state: {customer.state}")
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "seated"
                    customer.face_to(customer.face_direction)
                    self.log(f"【着座】id: {customer.id} state: {customer.state}")

    # 着席中の顧客の飲食時間をカウントし、一定時間経過したら退店へ移行する関数
    def eating(self, dt):
        for customer in self.customers:
            if customer.state == "seated":
                customer.stay_timer += dt
                if customer.stay_timer >= STAY_DURATION:
                    # 退店へ
                    exit_x, exit_y = self.parent.map.exit_pos_list[0]  # 複数あるならランダムでもOK
                    customer.set_new_target(exit_x, exit_y)
                    customer.state = "leaving"
                    # customer.sprite.color = (90,142,71)
                    self.log(f"【出口移動開始】id: {customer.id} Exit pos: {exit_x, exit_y} state: {customer.state}")  

                    # 座席の解放
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == customer:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
                            self.log(f"【座席解放】id: {customer.id} seat: [{seat_i}]") 

    # 退店処理（出口に移動し終わったらリストから削除）
    def move_to_exit(self, dt):
        for customer in self.customers:
            if customer.state == "leaving":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "exited"
                    self.log(f"【退店】id: {customer.id} state: {customer.state}")

    # 座席の占用率を取得する関数
    def get_seat_occupancy(self):
        occupied_seats = sum(self.seat_in_use)
        total_seats = len(self.seat_in_use)
        return occupied_seats / total_seats if total_seats > 0 else 0

    # 顧客の込み具合を表示するラベルの更新
    def update_crowd_label(self):
        occupancy = self.get_seat_occupancy()
        percentage = int(occupancy * 100)
        # 混雑度ラベルのテキストを更新
        self.parent.map.crowd_label.text = f"混雑度: {percentage}%"
