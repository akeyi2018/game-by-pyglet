from settings import *
from loguru import logger
from seat_model import SeatArea
from pyglet.event import EventDispatcher

# 座席管理クラス
class SeatManager(EventDispatcher):

    def __init__(self, parent, log_func=None):
        super().__init__() # EventDispatcherの初期化を呼び出す

        # parentはMainGameクラスのインスタンスを想定
        self.parent = parent

        # MAP上の座席の座標リスト
        self.seat_positions = parent.map.seat_pos

        # 座席モデルの初期化
        self.seat_area = SeatArea(self.seat_positions)

        self.customer_manager = self.parent.customer_manager  # 顧客管理クラスへの参照
        # 顧客リストと顧客管理の参照
        self.customers = self.customer_manager.customers
        # 待機場所クラスへの参照
        self.wait_area = self.customer_manager.wait_area

    # 座席の割当、移動、飲食時間のカウント、退店処理を行うupdate関数
    def update(self, dt):

        # 座席に移動中の顧客を更新
        self.move_to_seat(dt)

        # 着席中の顧客の飲食時間をカウントし、一定時間経過したら退店へ移行
        self.eating(dt)

        # 退店処理
        self.move_to_exit(dt)

        # 混雑度ラベルの更新
        self.update_crowd_label()

    # dispatch_event('on_assign_to_seat', customer) で呼び出される関数
    def on_assign_to_seat(self, customer):
        self.assign_seat(customer)

                    
    # 特定の顧客に空いている座席を割り当てる関数
    def assign_seat(self, customer):
        
        # 空いている座席を探す
        for seat_idx, seat in enumerate(self.seat_area.seats):
            if not seat["in_use"]:
                # 1. 座席を占有状態にする
                self.seat_area.assign(seat_idx, customer.id)
                
                # 2. 顧客の移動ターゲットと状態を設定
                target = seat["grid"]
                customer.set_new_target(*target)
                customer.state = "moving_to_seat"
                customer.face_direction = seat["facing"]
                logger.info(f"【座席割当】id:{customer.id} → seat[{seat_idx}] pos:{target} state:{customer.state}")
                
                # 3. 待機場所の占有状態を解放して、列を詰める
                self.wait_area.release_by_customer(customer) 
                self.wait_area.shift_waiting_customers_forward()
                return

    # 顧客を座席に移動させる関数
    def move_to_seat(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_seat":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "seated"
                    customer.face_to(customer.face_direction)
                    logger.info(f"【着座】id: {customer.id} state: {customer.state}")

    # 着席中の顧客の飲食時間をカウントし、一定時間経過したら退店へ移行する関数
    def eating(self, dt):
        for customer in self.customers:
            if customer.state == "seated":
                customer.stay_timer += dt
                if customer.stay_timer >= STAY_DURATION:
                    # 退店へ
                    exit_x, exit_y = self.parent.map.exit_pos_list[0]  # 複数あるなら最短/ランダム選択に拡張可
                    customer.set_new_target(exit_x, exit_y)
                    customer.state = "leaving"
                    logger.info(f"【出口移動開始】id: {customer.id} Exit pos: {(exit_x, exit_y)} state: {customer.state}")

                    # 使っていた座席の解放
                    for seat_idx, seat in enumerate(self.seat_area.seats):
                        if seat["customer_id"] == customer.id:
                            self.seat_area.release(seat_idx)
                            logger.info(f"【座席解放】id: {customer.id} seat: [{seat_idx}]")
                            break  # 座席は1つだけなので見つけたらループ抜け

    # 退店処理（出口に移動し終わったらリストから削除）
    def move_to_exit(self, dt):
        for customer in self.customers:
            if customer.state == "leaving":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "exited"
                    logger.info(f"【退店】id: {customer.id} state: {customer.state}")

    # 座席の占用率を取得する関数
    def get_seat_occupancy(self):
        # in_use=True の座席の数を数えて全座席数で割る
        occupied_count = sum(1 for seat in self.seat_area.seats if seat["in_use"])
        return occupied_count / len(self.seat_area.seats) if self.seat_area.seats else 0.0

    # 顧客の込み具合を表示するラベルの更新
    def update_crowd_label(self):
        percentage = int(self.get_seat_occupancy() * 100)
        self.parent.map.crowd_label.text = f"座席の占用率: {percentage}%"