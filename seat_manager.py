from settings import *
from loguru import logger
from seat_model import SeatArea

# 座席管理クラス
class SeatManager:

    def __init__(self, parent, log_func=None):
        # parentはMainGameクラスのインスタンスを想定
        self.parent = parent

        # ---- 座席モデル（シンプル版 SeatArea） ----
        # self.seat_positions = parent.map.seat_pos
        # # 偶数:右 / 奇数:左 の簡易ルール（必要に応じて変更可）
        # self.facings = [('right' if i % 2 == 0 else 'left') for i, _ in enumerate(self.seat_positions)]
        # self.seat_area = SeatArea(self.seat_positions, facings=self.facings)

        # MAP上の座席の座標リスト
        self.seat_positions = parent.map.seat_pos
        # 座席管理リスト(使われているかどうか)
        self.seat_in_use = [False] * len(self.seat_positions)
        # 座席キュー（顧客と座席の紐づけ）: 退店時に座席を解放するための追跡用途
        self.seat_queue = []

        self.customer_manager = self.parent.customer_manager  # 顧客管理クラスへの参照

        # 顧客リストと顧客管理の参照
        self.customers = self.customer_manager.customers

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
        for customer, wait_idx in self.customer_manager.waiting_queue:
            if customer.state == "waiting_for_seat":
                for seat_idx, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        # 座席を占有状態にする
                        self.seat_in_use[seat_idx] = True
                        # 顧客が移動するターゲットを座席に設定
                        target = self.seat_positions[seat_idx]
                        customer.set_new_target(*target)
                        customer.state = "moving_to_seat"
                        customer.face_direction = 'right' if seat_idx % 2 == 0 else 'left'
                        self.seat_queue.append((customer, seat_idx))
                        logger.info(f"【座席割当】id:{customer.id} → seat[{seat_idx}] pos:{target} facing:{customer.face_direction}")
                        
                        # 待機場所の占有状態を解放
                        self.customer_manager.wait_pos_in_use[wait_idx] = False
                        # 待機キューからこの顧客を削除
                        self.customer_manager.waiting_queue.remove((customer, wait_idx))
                        # 待機顧客を詰める（後ろの顧客を前に1人だけ詰める）
                        self.customer_manager.shift_waiting_customers_forward()
                        return


        #     if customer.state == "waiting_for_seat":
        #         logger.info(f"【座席割当開始】id:{customer.id} state:{customer.state}")
        #         self.assign_seat_to_customer(customer)
        # # ④ 座席に空きがない場合は何もしない（最初に判定して即リターン）
        # seat_idx = self.seat_area.first_free_index()
        # if seat_idx is None:
        #     return

        # # ① 待機場所の先頭に顧客がいる場合のみ続行（いなければ何もしない）
        # head_id = self.cm.wait_area.head_customer_id()
        # if head_id is None:
        #     return

        # # 顧客インスタンス取得（存在しなければ何もしない）
        # customer = next((c for c in self.customers if c.id == head_id), None)
        # if customer is None:
        #     return

        # # ② 先頭の待機スポットを解放
        # head_spot_idx = self.cm.wait_area.get_spot_of(head_id)
        # if head_spot_idx is None:
        #     return
        # # ③ 2番目の顧客を先頭に「1人だけ」前詰め（戻り値があれば、その顧客だけ移動命令）
        # move = self.cm.wait_area.release_and_shift_one(head_spot_idx)
        # logger.info(f"【待機スポット解放】id:{customer.id} spot:[{head_spot_idx}]")

        # if move:
        #     cid, from_i, to_i = move
        #     shifted = next((c for c in self.customers if c.id == cid), None)
        #     if shifted:
        #         target = self.cm.wait_area.get_grid(to_i)
        #         shifted.set_new_target(*target)
        #         shifted.state = "moving_to_wait"
        #         logger.info(f"【詰め移動】id:{shifted.id} W[{from_i}]→W[{to_i}] pos:{target}")

        # ここまで来たら、空席があり、先頭が存在して解放済み
        # 座席を占有して先頭顧客を席へ案内
        # self.seat_area.occupy(seat_idx, customer.id)

        # seat_pos = self.seat_area.get_grid(seat_idx)
        # customer.set_new_target(*seat_pos)
        # customer.state = "moving_to_seat"
        # customer.face_direction = self.seat_area.get_facing(seat_idx)

        # self.seat_queue.append((customer, seat_idx))
        # logger.info(f"【座席割当】id:{customer.id} → seat[{seat_idx}] pos:{seat_pos} facing:{customer.face_direction}")

    # 顧客を座席に移動させる関数
    def move_to_seat(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_seat":
                logger.info(f"【席移動開始】id: {customer.id} state: {customer.state}")
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
                    for idx, (cust_obj, seat_i) in enumerate(self.seat_queue):
                        if cust_obj == customer:
                            self.seat_in_use[seat_i] = False
                            self.seat_queue.pop(idx)
                            logger.info(f"【座席解放】id: {customer.id} seat: [{seat_i}]")
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
        # in_use_flags の合計から計算してもよいが、SeatArea の occupancy_ratio を使う方が簡潔
        return self.seat_in_use.count(True) / len(self.seat_in_use) if self.seat_in_use else 0.0

    # 顧客の込み具合を表示するラベルの更新
    def update_crowd_label(self):
        percentage = int(self.get_seat_occupancy() * 100)
        self.parent.map.crowd_label.text = f"混雑度: {percentage}%"