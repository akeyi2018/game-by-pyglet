# プログラム全体ドキュメントインデックス

このドキュメントでは、シミュレーションカフェプログラムの主要クラスの概要とリンクを示します。

---

## 1. Main クラス
- ファイル: `main.py`
- 役割: Pygletウィンドウ管理、全体のイベントループ、各マネージャーの初期化
- 主な機能:
  - ウィンドウ生成
  - 描画バッチ管理
  - CustomerManager / SeatManager の更新
  - キー操作・マウス操作のイベントハンドリング
  - ログ管理
- 主なメソッド:
  - `__init__`
  - `update(dt)`
  - `on_draw()`
  - `on_mouse_press(x, y, button, modifiers)`
  - `on_key_press(symbol, modifiers)`
  - `close()`

---

## 2. Map クラス
- ファイル: `map.py`
- 役割: マップデータ管理、通行可能セル判定、待機/座席/出口座標管理
- 主な変数:
  - `map_data`, `cell_size`, `batch`, `window_height`
  - `wait_pos`, `seat_pos`, `table_pos`, `customer_pos`
  - `tiles`, `buttons`, `open_doors`, `cust_label`, `exit_pos_list`
- 主なメソッド:
  - `load_map()`
  - `on_mouse_press(x, y, button, modifiers)`
  - `button_clicked(x, y, is_open)`
  - `is_walkable(x, y)`
  - `get_random_customer_positions(num, area_rows)`
  - `get_exit_positions()`
  - `get_entrance_positions()`

---

## 3. CustomerManager クラス
- ファイル: `customerManager.py`
- 役割: 顧客生成、入口/待機場所割当、移動管理、削除
- 主な変数:
  - `customers`, `waiting_queue`, `wait_pos_in_use`
  - `spawn_timer`, `spawn_interval`, `num_customers_to_initialize`
- 主なメソッド:
  - `setup_initial_customers()`
  - `update(dt)`
  - `spawn_customer()`
  - `assign_to_entrance()`
  - `move_to_entrance(dt)`
  - `assign_to_wait_pos()`
  - `move_to_wait_pos(dt)`
  - `delete_customer()`
  - `shift_waiting_customers_forward()`

---

## 4. SeatManager クラス
- ファイル: `seat_manager.py`
- 役割: 座席管理、着座中の滞在管理、退店処理
- 主な変数:
  - `seat_positions`, `seat_in_use`, `seat_queue`
  - `customers` (CustomerManager参照)
- 主なメソッド:
  - `update(dt)`
  - `assign_seat()`
  - `move_to_seat(dt)`
  - `eating(dt)`
  - `move_to_exit(dt)`

---

## 5. Customer クラス
- ファイル: `customer.py`
- 役割: 顧客単体の状態管理、位置・移動・アニメーション管理
- 主な変数:
  - `id`, `grid_x`, `grid_y`, `target_pos_x`, `target_pos_y`
  - `state`, `color`, `face_direction`, `sprite`, `frames`, `sheet`
  - `moving`, `move_timer`, `move_duration`, `stay_timer`
- 主なメソッド:
  - `update(dt, game_map)`
  - `move_target(game_map, dt)`
  - `start_moving_to(new_x, new_y)`
  - `face_to(direction)`
  - `set_new_target(target_x, target_y)`
  - `reached_final_target` (プロパティ)
