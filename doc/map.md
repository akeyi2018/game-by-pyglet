

---

# マップクラス (Map) 設計書

## 役割

* 店舗全体のマップを構築・管理する。
* 各セル情報に応じて、床、テーブル、座席、待機列、ドアなどを初期化する。
* 顧客の移動可能領域を判定し、入退店位置を提供する。
* ドアの開閉やマウス操作もハンドリングする。

---

| 変数名             | 型                     | 説明                          |
| --------------- | --------------------- | --------------------------- |
| `map_data`      | list\[list]           | MAP\_DATA（マップ文字列）           |
| `cell_size`     | int                   | 1マスのピクセルサイズ                 |
| `batch`         | pyglet.graphics.Batch | 描画バッチ                       |
| `window_height` | int                   | ウィンドウ高さ                     |
| `tiles`         | list                  | スプライト / 矩形 / ラベルなどの描画オブジェクト |
| `wait_pos`      | list\[tuple]          | 待機ポジションのグリッド座標リスト           |
| `customer_pos`  | list\[tuple]          | 顧客生成可能位置リスト                 |
| `table_pos`     | list\[tuple]          | テーブル座標リスト                   |
| `seat_pos`      | list\[tuple]          | 座席座標リスト                     |
| `table_image`   | pyglet.image.Image    | テーブル画像                      |
| `floor_image`   | pyglet.image.Image    | フロア画像                       |
| `kusa`          | pyglet.image.Image    | 草原画像（店外）                    |
| `buttons`       | list                  | DoorButtonオブジェクトリスト         |
| `open_doors`    | set                   | 開いているドアの座標セット               |
| `cust_label`    | pyglet.text.Label     | 来客数表示ラベル                    |
| `exit_pos_list` | list\[tuple]          | 退店位置の座標リスト                  |

---

## セル種別と処理対応

* `'B'` : 壁 → 通行不可
* `'D'` : ドアボタンを配置
* `'W'` : 待機位置（`wait_pos` に登録）
* `'L'` : ラベル（来客数表示ラベルを設置）
* `'T'` : テーブル配置（`table_pos` に登録、通行不可）
* `'S'` : 座席配置（`seat_pos` に登録）
* `'.'` : 床配置（通行可）
* `'F'` : 草原（屋外エリア、入場経路などに利用）
* `'O'` : 出口位置（`exit_pos_list` に登録）

---

## 主な処理

### `__init__(batch, window_height)`

* マップデータの読み込み・描画用スプライトの生成
* テーブル、床、座席、待機位置などの初期化
* `load_map()` 呼び出し

---

### `load_map()`

* `map_data` を走査して各セルを処理し、描画スプライトや座標リストを生成
* 待機列 (`wait_pos`) を逆順にして、行列の整列順序を確保
* 出口位置を取得 (`exit_pos_list`)

---

### `on_mouse_press(x, y, button, modifiers)`

* マウスクリック時の処理
* ドアボタンがクリックされたか判定し、クリックイベントを実行

---

### `button_clicked(x, y, is_open)`

* ドアの開閉状態を管理
* ドアが開いたら `open_doors` に座標追加、閉じたら削除

---

### `is_walkable(x, y)`

* 顧客が通行可能か判定

  * 壁・テーブル → 不可
  * ドア → 開いていれば可
  * その他のセル → 可

---

### `get_random_customer_positions(num_customers, area_rows=(1, 4))`

* 草原エリア(`'F'`)からランダムに顧客生成位置を選ぶ
* 指定行範囲 (`area_rows`) 内で `num_customers` 人分を返す

---

### `get_exit_positions()`

* マップ内の `'O'` セルを全て取得 → 退店口として返す

---

### `get_entrance_positions()`

* マップ内の `'L'` セルを全て取得 → 入店口として返す

---

## 補足

* **顧客待機列**: `'W'` セルで定義、逆順管理で先頭詰め処理を考慮
* **入退店位置**: `'L'`（入口）、`'O'`（出口）で判定
* **ドア開閉**: `DoorButton` 経由で制御

---

