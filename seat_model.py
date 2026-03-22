# seat_model.py (simple)

from typing import List, Optional, Tuple, Iterable

Grid = Tuple[int, int]

class SeatArea:
    """
    シンプル座席モデル：
      - 内部は [{'grid': (x,y), 'facing': 'right'|'left', 'customer_id': None|int}, ...]
      - 提供APIは最小限（空席検索・占有・解放・参照・利用率）
    """
    def __init__(self,
                 seat_positions: Iterable[Grid],
                 facings: Optional[Iterable[str]] = None):
        # 座席の座標
        self.pos_list = list(seat_positions)

        # 顔の向き(奇数番目は右向き、偶数番目は左向きなどのルールで自動生成も可能)
        self.facing_list = ['right' if i % 2 == 0 else 'left' for i in range(len(self.pos_list))] if facings is None else list(facings)

        self.seats: List[dict] = [
            {"grid": self.pos_list[i], 
             "facing": self.facing_list[i], 
             "customer_id": None,
             "in_use": False}  # 追加: 占有フラグ
            for i in range(len(self.pos_list))
        ]
    
    # 座席の空きを検索する関数
    def first_free_index(self) -> Optional[int]:
        for i, s in enumerate(self.seats):
            if s["customer_id"] is None:
                return i
        return None
    
    # 顧客IDから座席インデックスを検索する関数
    def get_seat_of(self, customer_id: int) -> Optional[int]:
        for i, s in enumerate(self.seats):
            if s["customer_id"] == customer_id:
                return i
        return None
    
    # 座席を占有する関数
    def assign(self, index: int, customer_id: int):
        if index is not None and customer_id is not None and 0 <= index < len(self.seats):
            self.seats[index]["customer_id"] = customer_id
            self.seats[index]["in_use"] = True  # 占有フラグを立てる
        
    def release(self, index: int):
        if index is not None and 0 <= index < len(self.seats):
            self.seats[index]["customer_id"] = None
            self.seats[index]["in_use"] = False  # 占有フラグもリセット