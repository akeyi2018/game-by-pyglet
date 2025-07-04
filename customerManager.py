from settings import *
from customer import Customer
import time
import pyglet

class CustomerManager:
    def __init__(self, parent, num_customers=2, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch

        self.customer_pos_list = parent.map.get_random_customer_positions(num_customers)
        
        # 出口の位置
        self.exit_pos_list = parent.map.get_exit_positions()

        # 入口の位置
        self.entrance_pos = parent.map.get_entrance_positions()

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
        self.customer_count = 0

        # 初期顧客
        self.setup_initial_customers()

    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()

    def update(self, dt):

        # 入口まで割り当て
        self.assign_to_entrance()

        # 入口まで移動
        self.move_to_entrance(dt)

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
        customer = Customer(customer_pos, state, self.window_height, self.cell_size, self.color, self.batch)
        self.customers.append(customer)
        self.log(f"【顧客生成】id: {customer.id} pos: {customer_pos} state: {state}")

    def assign_to_entrance(self):
        for customer in self.customers:
            if customer.state == "outside":
                target = self.entrance_pos[0]
                customer.set_new_target(*target)
                customer.state = "moving_to_entrance"
                self.log(f"【店入口割当】id: {customer.id} pos: {target} \
                                state: {customer.state}")
    
    def move_to_entrance(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_entrance":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "arrive"
                
                    self.log(f"【店到着】id: {customer.id} pos: {customer.grid_x, customer.grid_y} \
                                state: {customer.state}")

    def assign_to_wait_pos(self):
        # Step 1: W に空きがあれば、outside → moving_to_wait にする
        # 入口の座標
        entrance_x, entrance_y = self.entrance_pos[0]

        closest_customer = None
        distance = 10000
        for customer in self.customers:
            if customer.state == "arrive":
                # 最も近い人を待機場所へ割り当てる
                for j, used in enumerate(self.wait_pos_in_use):
                    if not used:
                        self.wait_pos_in_use[j] = True
                        self.waiting_queue.append((customer, j))
                        target = self.wait_pos_list[j]
                        customer.set_new_target(*target)
                        customer.state = "moving_to_wait"
                        customer.sprite.color = (90,142,71)
                        self.log(f"【待機場所割当】id: {customer.id} index: W[{j}] pos: {target} \
                                state: {customer.state}")
                        break  # 1人だけWに入れる

    def move_to_wait_pos(self, dt):
        # Step 2: moving_to_wait → waiting に状態変更
        for customer, wait_i in self.waiting_queue:
            if customer.state == "moving_to_wait":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    if wait_i == 0:
                        customer.state = "waiting"
                    else:
                        customer.state = "waiting_for_top"
                    self.log(f"【待機場所到着】id: {customer.id} index: W[{wait_i}] state: {customer.state}")

    def delete_customer(self):
        # 顧客の削除処理
        for i, customer in enumerate(self.customers):
            if customer.state == "exited":
                self.customer_count += 1
                self.parent.map.cust_label.text = f"来客数:{self.customer_count}"
                self.log(f"【顧客削除】id: {customer.id}")
                self.customers.pop(i)


    def shift_waiting_customers_forward(self):
        # 待機列を wait_i 昇順でチェック
        for i in range(len(self.wait_pos_in_use)):
            if not self.wait_pos_in_use[i]:
                # 後ろの顧客を詰める
                for idx, (customer, current_i) in enumerate(self.waiting_queue):
                    if current_i > i:
                        self.waiting_queue[idx] = (customer, i)
                        self.wait_pos_in_use[current_i] = False
                        self.wait_pos_in_use[i] = True
                        customer.set_new_target(*self.wait_pos_list[i])
                        customer.state = "moving_to_wait"
                        self.log(f"【詰め移動】id: {customer.id} from W[{current_i}] → W[{i}]")
                        break  # 1人だけ詰める
