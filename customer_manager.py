from settings import *
from customer import Customer
from loguru import logger
from wait_model import WaitArea

# 顧客管理クラス
class CustomerManager:
    def __init__(self, parent, num_customers=10):
        self.parent = parent
        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch

        # --- 待機場所のモデル（シンプル版） ---
        self.wait_pos_list = parent.map.wait_pos
        # self.wait_area = WaitArea(self.parent.map.wait_pos) 

        # 入口の位置
        self.entrance_pos = parent.map.get_entrance_positions()

        # ☆ 旧: 並行配列ベースの待機管理 は廃止
        # self.wait_pos_list = parent.map.wait_pos
        self.waiting_queue = []
        self.wait_pos_in_use = [False] * len(self.wait_pos_list)

        # 顧客本体
        self.customers = []
        self.num_customers_to_initialize = num_customers

        # スポーン関連
        self.spawn_timer = 0.0
        self.spawn_interval = SPAWN_TIME
        self.max_customers = MAX_CUSTOMERS

        self.color = (0, 255, 255)
        self.customer_count = 0

        # 初期顧客
        self.setup_initial_customers()

    def setup_initial_customers(self):
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()

    def update(self, dt):
        # 入口まで割り当て
        self.assign_to_entrance()
        # 入口へ移動
        self.move_to_entrance(dt)
        # 待機場所へ割り当て
        self.assign_to_wait_pos()
        # 待機場所へ移動
        self.move_to_wait_pos(dt)
        # 退店顧客の削除
        self.delete_customer()
        # スポーン
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0.0
            if len(self.customers) < self.max_customers:
                self.spawn_customer()

    def spawn_customer(self):
        # 顧客生成エリア（店外）
        pos_list = self.parent.map.get_random_customer_positions(1)
        if not pos_list:
            logger.debug("顧客生成失敗：初期位置が取得できません")
            return

        customer_pos = pos_list[0]
        state = "outside"
        customer = Customer(customer_pos, state, self.window_height, self.cell_size, self.color, self.batch)
        self.customers.append(customer)
        logger.info(f"【顧客生成】id:{customer.id} pos:{customer_pos} state:{state}")

    # 入口に顧客を割り当てる
    def assign_to_entrance(self):
        for customer in self.customers:
            if customer.state == "outside":
                target = self.entrance_pos[0]
                customer.set_new_target(*target)
                customer.state = "moving_to_entrance"
                logger.info(f"【店入口割当】id:{customer.id} pos:{target} state:{customer.state}")

    # 入口に顧客を移動
    def move_to_entrance(self, dt):
        for customer in self.customers:
            if customer.state == "moving_to_entrance":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    customer.state = "arrive"
                    logger.info(f"【店到着】id:{customer.id} pos:{(customer.grid_x, customer.grid_y)} state:{customer.state}")

    # 待機場所へ割り当て（シンプル版 WaitArea に合わせる）
    def assign_to_wait_pos(self):
         for customer in self.customers:
            if customer.state == "arrive":
                # 最も近い顧客を待機場所に割り当てる
                for j, used in enumerate(self.wait_pos_in_use):
                    if not used:
                        # 待機場所用キューと顧客を紐づける
                        self.waiting_queue.append((customer, j))
                        # 待機場所を占有状態にする
                        self.wait_pos_in_use[j] = True
                        # 顧客が移動するターゲットを待機場所に設定
                        target = self.wait_pos_list[j]
                        customer.set_new_target(*target)
                        customer.state = "moving_to_wait"
                        logger.info(f"【待機場所割当】id:{customer.id} W[{j}] pos:{target} state:{customer.state}")
                        break

    # 待機場所へ移動（到着したら waiting / waiting_for_top へ遷移）
    def move_to_wait_pos(self, dt):
        for customer, wait_idx in self.waiting_queue:
            if customer.state == "moving_to_wait":
                customer.update(dt, self.parent.map)
                if not customer.is_moving and customer.reached_final_target:
                    # 先頭: waiting / それ以外: waiting_for_top
                    customer.state = "waiting_for_seat" if wait_idx == 0 else "waiting_for_top"
                    logger.info(
                        f"【待機場所到着】id:{customer.id} W[{wait_idx}] pos:{(customer.grid_x, customer.grid_y)} state:{customer.state}"
                    )

    def delete_customer(self):
        # 退店済みの顧客を削除（来客数ラベル更新）
        # ※ ループ中削除の安全のため enumerate の結果を list 化
        for i, customer in list(enumerate(self.customers)):
            if customer.state == "exited":
                self.customer_count += 1
                self.parent.map.cust_label.text = f"来客数:{self.customer_count}"
                logger.info(f"【顧客削除】id:{customer.id}")
               
                # 安全削除（必ず safe_delete_sprite を通す）
                if hasattr(customer, 'safe_delete_sprite'):
                    customer.safe_delete_sprite()
                else:
                    # フラグ未導入でも落ちないように最低限の防御
                    try:
                        if getattr(customer, 'sprite', None) and getattr(customer.sprite, '_vertex_list', None):
                            customer.sprite.delete()
                    except Exception as e:
                        logger.warning(f"[sprite delete fallback] id:{customer.id} err:{e}")
                    finally:
                        customer.sprite = None

                # リストから取り除く
                self.customers.pop(i)


    # （任意）待機占有率：WaitArea が超シンプル構成なのでここで計算しても OK
    def get_waiting_occupancy(self):
        if not self.wait_area.spots:
            return 0.0
        used = sum(1 for s in self.wait_area.spots if s["customer_id"] is not None)
        return used / len(self.wait_area.spots)
    
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
                        logger.info(f"【詰め移動】id: {customer.id} from W[{current_i}] → W[{i}]")
                        break  # 1人だけ詰める
