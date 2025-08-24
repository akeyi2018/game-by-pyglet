
---

# プログラム詳細設計書

## 1. プログラム名

`customerManager.py`

## 2. 処理概要

カフェシミュレーションにおける顧客の生成・移動・削除を管理する。
顧客は「店外 → 入口 → 待機場所 → 座席 → 退店」というライフサイクルを持つ。
本クラスは待機列の管理も担い、座席に移動するまでの顧客の状態遷移を制御する。

---

## 3. 処理詳細

### 3.1 インポートモジュール

* **settings**: シミュレーション定数（CELL\_SIZE, SPAWN\_TIME, MAX\_CUSTOMERS など）
* **customer.Customer**: 顧客を表すクラス
* **time**: 経過時間やログ用（現状は利用箇所は少ない）
* **pyglet**: スプライト描画で使用

---

### 3.2 クラス名

`CustomerManager`

---

### 3.3 メソッド一覧

| No | Name                              | 説明                        | 備考         |
| -- | --------------------------------- | ------------------------- | ---------- |
| 1  | `__init__`                        | 初期化処理。入口/待機場所/顧客リストなどをセット | 外部から呼び出される |
| 2  | `setup_initial_customers`         | 初期顧客を生成                   | class内部使用  |
| 3  | `update`                          | 毎フレーム呼び出され、全体の状態遷移を制御     | 外部から呼び出される |
| 4  | `spawn_customer`                  | 新規顧客を生成し、店外に配置            | class内部使用  |
| 5  | `assign_to_entrance`              | 店外の顧客を入口に割り当て             | class内部使用  |
| 6  | `move_to_entrance`                | 顧客を入口に移動させ、到着後に状態を更新      | class内部使用  |
| 7  | `assign_to_wait_pos`              | 入口到着済みの顧客を待機場所に割り当て       | class内部使用  |
| 8  | `move_to_wait_pos`                | 待機場所へ移動中の顧客を状態更新          | class内部使用  |
| 9  | `delete_customer`                 | 退店済みの顧客を削除                | class内部使用  |
| 10 | `shift_waiting_customers_forward` | 待機列に空きが出た際、顧客を前に詰める       | class内部使用  |

---

### 3.3.1 コンストラクタ (`__init__`)

**引数**

| No | Name           | 型    | 説明                     |
| -- | -------------- | ---- | ---------------------- |
| 1  | parent         | obj  | メインアプリ (`Main`) インスタンス |
| 2  | num\_customers | int  | 初期生成する顧客数              |
| 3  | log\_func      | func | ログ関数（指定なしなら無効化）        |

**処理内容**

* 親 (`parent`) から必要な情報（ウィンドウ高さ、batch、map情報）を取得
* 入口座標を取得し保持
* 待機場所のリストと利用状況フラグを初期化
* 顧客リスト、生成タイマー、生成間隔、最大顧客数を設定
* 初期顧客を `setup_initial_customers()` により生成

---

### 3.3.2 `setup_initial_customers`

**引数**: なし
**戻り値**: なし

**処理内容**

* `num_customers_to_initialize` の人数分 `spawn_customer()` を呼び出し、初期顧客を生成

---

### 3.3.3 `update`

**引数**

| No | Name | 型     | 説明               |
| -- | ---- | ----- | ---------------- |
| 1  | dt   | float | 前回フレームからの経過時間（秒） |

**処理内容**

* 顧客を入口に割り当て (`assign_to_entrance`)
* 入口まで移動させる (`move_to_entrance`)
* 待機場所に割り当て (`assign_to_wait_pos`)
* 待機場所まで移動 (`move_to_wait_pos`)
* 退店済みの顧客削除 (`delete_customer`)
* スポーンタイマーを進め、新規顧客を一定間隔で生成

---

### 3.3.4 `spawn_customer`

**引数**: なし
**戻り値**: なし

**処理内容**

* ランダムに顧客生成位置を取得（店外の座標）
* 失敗時はログにエラーを出して終了
* 成功時は `Customer` インスタンスを生成し、state を `"outside"` に設定
* `customers` リストに追加し、ログを出力

---

### 3.3.5 `assign_to_entrance`

**引数**: なし
**戻り値**: なし

**処理内容**

* `state == "outside"` の顧客に入口座標をセット
* 顧客の状態を `"moving_to_entrance"` に変更し、ログを出力

---

### 3.3.6 `move_to_entrance`

**引数**: `dt`
**処理内容**

* `state == "moving_to_entrance"` の顧客を更新し、移動完了を確認
* 入口に到着した顧客の状態を `"arrive"` に変更
* ログを出力

---

### 3.3.7 `assign_to_wait_pos`

**引数**: なし
**処理内容**

* `state == "arrive"` の顧客を対象に、未使用の待機場所を検索
* 最初に空いている場所を見つけたら割り当て
* 顧客の状態を `"moving_to_wait"` に変更
* `waiting_queue` に `(顧客, index)` を追加し、ログを出力

---

### 3.3.8 `move_to_wait_pos`

**引数**: `dt`
**処理内容**

* `state == "moving_to_wait"` の顧客を更新し、到着判定を実施
* 到着した顧客を `"waiting"` または `"waiting_for_top"` に変更（W\[0] が特別扱い）
* ログを出力

---

### 3.3.9 `delete_customer`

**引数**: なし
**処理内容**

* `state == "exited"` の顧客を削除対象とする
* 来客数カウンタを増加し、ラベルを更新
* スプライトが残っていれば削除
* 顧客リストから該当オブジェクトを除去

---

### 3.3.10 `shift_waiting_customers_forward`

**引数**: なし
**処理内容**

* 待機場所リストを順に確認し、空きがある場合は後ろの顧客を前に詰める
* 顧客の待機場所インデックスを更新し、新しいターゲット座標を再設定
* 状態を `"moving_to_wait"` に戻す
* ログを出力

---

## 3.4 外部インターフェース

### 3.4.1 インスタンス宣言

```python
customer_manager = CustomerManager(parent, num_customers=2, log_func=logger)
```

### 3.4.2 更新処理

```python
customer_manager.update(dt)
```

顧客は生成され、入口 → 待機場所へ移動し、退店すれば削除される。

---
