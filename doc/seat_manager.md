

---

# 座席マネージャー（SeatManager）設計書

## クラス概要

`SeatManager` は店舗マップ上の **座席の割当・管理** を担当するクラス。
顧客が「待機 → 座席 → 食事 → 退店」する一連の流れを座席視点で管理する。
座席の使用状況・キュー・顧客との紐付けを制御する。

---

## 管理対象

* **座席座標リスト**（`self.seat_positions`）
* **座席使用状況リスト**（`self.seat_in_use`）
* **座席キュー**（顧客と座席の紐づけ）
* **顧客リスト**（CustomerManager から参照）

---

## 属性（メンバ変数）

| 変数名              | 型                      | 説明                          |
| ---------------- | ---------------------- | --------------------------- |
| `parent`         | object                 | 親（主にマップやCustomerManagerを保持） |
| `log`            | function               | ログ出力関数                      |
| `seat_positions` | list\[(x, y)]          | マップ上の座席座標                   |
| `seat_in_use`    | list\[bool]            | 各座席が使用中かどうか                 |
| `seat_queue`     | list\[(Customer, int)] | 顧客と座席番号のペア                  |
| `customers`      | list\[Customer]        | CustomerManager が保持する顧客リスト  |

---

## 状態遷移（顧客の座席に関する流れ）

```
waiting (待機)
   │
   ▼
moving_to_seat (席に移動中)
   │
   ▼
seated (着座 → 食事中)
   │
   ▼
leaving (退店移動中)
   │
   ▼
exited (退店完了)
```

---

## 主なメソッド

### `update(dt)`

* 毎フレーム実行される処理。
* 以下の流れを順番に呼び出す：

  1. `assign_seat()` … 待機中の顧客に座席を割り当てる
  2. `move_to_seat(dt)` … 座席に移動させる
  3. `eating(dt)` … 食事時間をカウントし、一定時間経過で退店へ移行
  4. `move_to_exit(dt)` … 出口へ移動させ、退店を完了させる

---

### `assign_seat()`

* 待機中の顧客に空いている座席を割り当てる。
* 割当処理の流れ：

  * 待機キューから顧客を取り出す
  * 空いている座席を検索
  * 顧客に座席座標をセットし `moving_to_seat` に変更
  * 座席を使用中に設定
  * 座席キューに追加
  * 待機位置（W）を解放し、残りの待機顧客を前へ詰める
* ログ例：

  ```
  【座席割当】id: 3 → seat[1]
  ```

---

### `move_to_seat(dt)`

* 状態が `moving_to_seat` の顧客を座席まで移動させる。
* 移動が完了すると状態を `seated` に変更。
* 座席に着いたらキャラの向きを修正。
* ログ例：

  ```
  【席移動開始】id: 3 state: moving_to_seat
  【着座】id: 3 state: seated
  ```

---

### `eating(dt)`

* 状態が `seated` の顧客に対して滞在時間（食事時間）を加算。
* `STAY_DURATION` 経過したら退店へ移行。

  * 出口座標をセット
  * 状態を `leaving` に変更
  * 座席を解放し、`seat_in_use` を更新
* ログ例：

  ```
  【出口移動開始】id: 3 Exit pos: (5, 10) state: leaving
  【座席解放】id: 3 seat: [1]
  ```

---

### `move_to_exit(dt)`

* 状態が `leaving` の顧客を出口へ移動させる。
* 到着したら `exited` に変更。
* ログ例：

  ```
  【退店】id: 3 state: exited
  ```

---

## 拡張ポイント

* 複数の出口に対応（ランダム or 座席位置に近い出口を選択）
* 滞在時間（`STAY_DURATION`）を顧客ごとに変動させる
* 座席のグループ利用（複数人で同じテーブルに着座）

---

