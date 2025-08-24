# クラス設計書：Customer クラス

## クラス概要
`Customer` クラスは、店に来店する顧客キャラクターを表現する。  
位置情報、移動制御、スプライト描画、アニメーション管理を担当する。

---

## クラス構造

### クラス変数
- **_id_counter**: `int`  
  全インスタンス間で一意な顧客IDを管理するカウンタ。

---

| 変数名                            | 型                                              | 説明                                            |
| ------------------------------ | ---------------------------------------------- | --------------------------------------------- |
| `_id_counter`                  | int (class)                                    | 顧客IDのカウンタ（クラス変数、一意なID管理）                      |
| `id`                           | int                                            | 顧客固有ID                                        |
| `grid_x`, `grid_y`             | int                                            | グリッド上の現在座標                                    |
| `target_pos_x`, `target_pos_y` | int                                            | 移動目標座標                                        |
| `cell_size`                    | int                                            | 1マスのピクセルサイズ                                   |
| `window_height`                | int                                            | ウィンドウの高さ（描画座標変換用）                             |
| `state`                        | str                                            | 顧客の状態（spawned / moving / waiting / seated など） |
| `color`                        | tuple                                          | 顔色または矩形色 (R,G,B)                              |
| `face_direction`               | str                                            | 向き（'up', 'down', 'left', 'right'）             |
| `sheet`                        | SpriteSheet                                    | アニメーション用スプライトシート                              |
| `frames`                       | list                                           | 現在方向のアニメーションフレームリスト                           |
| `sprite`                       | pyglet.sprite.Sprite / pyglet.shapes.Rectangle | 描画用スプライト                                      |
| `current_frame`                | int                                            | 現在のアニメーションフレーム番号                              |
| `elapsed_time`                 | float                                          | アニメーション経過時間                                   |
| `animation_speed`              | float                                          | アニメーション切替速度                                   |
| `moving`                       | bool                                           | 移動中かどうか                                       |
| `move_duration`                | float                                          | 移動完了までの時間                                     |
| `move_timer`                   | float                                          | 移動時間計測用タイマー                                   |
| `start_pixel`                  | tuple                                          | 移動開始時のピクセル座標                                  |
| `dest_pixel`                   | tuple                                          | 移動終了時のピクセル座標                                  |
| `stay_timer`                   | float                                          | 着席時間計測用（退店判定）                                 |

---

## 主なメソッド

### `__init__(...)`
- 初期化処理。
- 画像フォルダからランダムにキャラクターを選択。  
  該当ファイルがなければ矩形で代用。

---

### `update_animation(dt)`
- 経過時間に応じてフレームを更新する。

---

### プロパティ
- **is_moving**: `bool`  
  移動中かどうかを返す。
- **reached_final_target**: `bool`  
  最終目的地に到着したかどうかを返す。

---

### `start_moving_to(new_x, new_y)`
- 新しい座標 `(new_x, new_y)` に向けて移動開始。  
- 移動方向に応じてアニメーションを切り替える。

---

### `face_to(direction)`
- 明示的にキャラクターの向きを変更。

---

### `move_target(game_map, dt)`
- 現在の目的地に向けて移動処理を行う。
- 進行可能かどうかは `game_map.is_walkable()` で判定。

---

### `update(dt, game_map)`
- 移動処理とアニメーション更新を行う。

---

### `set_new_target(target_x, target_y)`
- 新しい移動目標を設定する。

---

## 状態遷移例
1. **outside**: 店外にいる状態。  
2. **moving_to_entrance** → **arrive**: 店入口へ移動。  
3. **moving_to_wait** → **waiting / waiting_for_top**: 待機列へ移動。  
4. **exited**: 店から退店し、削除対象。

---

## 備考
- キャラクター画像が存在しない場合は **矩形描画**で代替。  
- 移動は **補間計算**で滑らかに表現。  
- 方向に応じてスプライトシートのアニメーションを切替可能。
