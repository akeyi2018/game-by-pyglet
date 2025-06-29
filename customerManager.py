from settings import *
from customer import Customer
import time

class CustomerManager:
    def __init__(self, parent, num_customers=2, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch

        self.customer_pos_list = parent.map.get_random_customer_positions(num_customers)
        self.exit_pos_list = parent.map.get_exit_positions()

        # MAP上の待機場所の座標リスト
        self.wait_pos_list = parent.map.wait_pos
        # 待機場所キュー（顧客と待機場所の紐づけ）
        self.waiting_queue = []
        # 待機場所管理リスト（使われているかどうか）  
        self.wait_pos_in_use = [False] * len(self.wait_pos_list)

        self.customers = [] # 顧客本体のリスト
        self.num_customers_to_initialize = num_customers

        # 新規顧客の生成
        self.spawn_timer = 0.0
        self.spawn_interval = SPAWN_TIME # 5秒ごとに新しい顧客を生成
        self.max_customers = MAX_CUSTOMERS    # 任意：上限を設定したい場合

        self.color = (0, 255, 255)

        # 初期顧客
        self.setup_initial_customers()

    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()

    def update(self, dt):

        # 待機場所への割り当て
        self.assign_to_wait_pos()

        # 待機場所への移動
        self.move_to_wait_pos(dt)

        # 顧客削除
        self.delete_customer()

        # スポーンタイマー更新
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            if len(self.customers) < self.max_customers:
                self.spawn_customer()

    def spawn_customer(self):
        # 顧客生成エリア（店外）を取得
        pos_list = self.parent.map.get_random_customer_positions(1)
        if not pos_list:
            print("[DEBUG] 顧客生成失敗：初期位置が取得できません")
            return

        customer_pos = pos_list[0]

        # 顧客生成(店外)
        state = "outside"
        customer = Customer(customer_pos, customer_pos, state, self.window_height, self.cell_size, self.color, self.batch)
        self.customers.append(customer)
        self.log(f"【顧客生成】id: {customer.id} pos: {customer_pos} state: {state}")

    def assign_to_wait_pos(self):
        # Step 1: W に空きがあれば、outside → moving_to_wait にする
        for customer in self.customers:
            if customer.state == "outside":
                for j, used in enumerate(self.wait_pos_in_use):
                    if not used:
                        self.wait_pos_in_use[j] = True
                        self.waiting_queue.append((customer, j))
                        target = self.wait_pos_list[j]
                        customer.set_new_target(*target)
                        customer.state = "moving_to_wait"
                        self.log(f"【待機場所割当】id: {customer.id} index: W[{j}] pos: {target} state: {customer.state}")
                        break  # 1人だけWに入れる

    def move_to_wait_pos(self, dt):
        # Step 2: moving_to_wait → waiting に状態変更
        for customer, wait_i in self.waiting_queue:
            if customer.state == "moving_to_wait":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "waiting"
                    self.log(f"【待機場所到着】id: {customer.id} index: W[{wait_i}] state: {customer.state}")

    def delete_customer(self):
        # 顧客の削除処理
        for i, customer in enumerate(self.customers):
            if customer.state == "exited":
                self.log(f"【顧客削除】id: {customer.id}")
                self.customers.pop(i)
