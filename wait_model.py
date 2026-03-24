from loguru import logger

class WaitAreas:
    def __init__(self, wait_pos_list):

        self.wait_pos_list = wait_pos_list
        self.wait_buffer = []
        self.use_lists = [False] * len(wait_pos_list)

    def assign_customer(self, customer):
        # 占用状態がFalseの待機場所を探す
        for idx, in_use in enumerate(self.use_lists):
            if not in_use:
                self.use_lists[idx] = True  # 占用状態をTrueにする
                self.wait_buffer.append((customer, idx))  # 待機キューに顧客と待機場所のインデックスを追加
                target = self.wait_pos_list[idx]
                customer.set_new_target(*target)
                customer.state = "moving_to_wait"  # 顧客の状態を待機中に設定
                logger.info(f"【待機場所割当】id:{customer.id} W[{idx}] pos:{target} state:{customer.state}")
                break
    
    def release(self, idx):
        if 0 <= idx < len(self.use_lists):
            self.use_lists[idx] = False  # 待機場所の占用状態を解放
            # 待機キューから該当する顧客を削除
            self.wait_buffer = [(cust, i) for cust, i in self.wait_buffer if i != idx]
            logger.info(f"【待機場所解放】W[{idx}]")

    def get_waiting_customers(self):
        # 待機キューにいる顧客のリストのうち先頭の顧客を返す
        if self.wait_buffer:
            return [self.wait_buffer[0][0]]

    def shift_waiting_customers_forward(self):
        # 待機列を wait_i 昇順でチェック
        for i in range(len(self.use_lists)):
            if not self.use_lists[i]:
                # 後ろの顧客を詰める
                for idx, (customer, current_i) in enumerate(self.wait_buffer):
                    if current_i > i:
                        self.wait_buffer[idx] = (customer, i)
                        self.use_lists[current_i] = False
                        self.use_lists[i] = True
                        customer.set_new_target(*self.wait_pos_list[i])
                        customer.state = "moving_to_wait"
                        logger.info(f"【詰め移動】id: {customer.id} from W[{current_i}] → W[{i}]")
                        break  # 1人だけ詰める