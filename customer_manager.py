from settings import *
from customer import Customer
from loguru import logger
import pyglet
from wait_model import WaitAreas

# 顧客管理クラス
class CustomerManager:
    def __init__(self, parent, num_customers=10):
        self.parent = parent
        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch

        # --- 待機場所 ---
        self.wait_pos_list = parent.map.wait_pos

        # 入口の位置
        self.entrance_pos = parent.map.get_entrance_positions()

        # 新手法
        self.wait_area = WaitAreas(self.wait_pos_list)

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
        # 待機場所の込み具合ラベル表示の更新
        self.update_waiting_occupancy_label()
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
                self.wait_area.assign_customer(customer)

    # 待機場所へ移動（到着したら waiting / waiting_for_top へ遷移）
    def move_to_wait_pos(self, dt):
        for customer, wait_idx in self.wait_area.wait_buffer:
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

                # 来客数でシミュレーション終了
                if self.customer_count >= END_NUM_CUSTOMER:
                    logger.info(f"来客数が{END_NUM_CUSTOMER}人を超えました。シミュレーションを終了します。")
                    pyglet.app.exit()

    # （任意）待機占有率：WaitArea が超シンプル構成なのでここで計算しても OK
    def get_waiting_occupancy(self):
        if not self.wait_area.use_lists:
            return 0.0
        used = sum(1 for used in self.wait_area.use_lists if used)
        return used / len(self.wait_area.use_lists)

    def update_waiting_occupancy_label(self):
        occupancy = self.get_waiting_occupancy()
        self.parent.map.wait_label.text = f"待機占有率:{occupancy:.0%}"
