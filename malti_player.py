from pyglet.event import EventDispatcher

class Character(EventDispatcher):
    def __init__(self, name, num_items=0):
        super().__init__()
        self.name = name
        self.num_items = num_items
        # 自分がアイテムを「渡す」というイベントを登録
        self.register_event_type('on_give_item')

    def give_item_to(self, target):
        """指定した相手（target）にアイテムを渡す"""
        if self.num_items > 0:
            print(f"\n★ {self.name} から {target.name} へ薬草の譲渡を開始します")
            # イベント発火時に、引数として「渡し先のインスタンス」を一緒に送る
            self.dispatch_event('on_give_item', target)
        else:
            print(f"\n❌ {self.name} は薬草を持っていないため渡せません")

    def on_give_item(self, target):
        """自分がイベントを発火させた時に自動で呼ばれる処理"""
        self.num_items -= 1  # 自分のアイテムを減らす
        print(f" -> {self.name}: 薬草を渡しました (残り: {self.num_items})")
        
        # 引数で受け取った相手の「受け取り処理」を直接呼び出す
        target.receive_item(from_char=self)

    def receive_item(self, from_char):
        """相手からアイテムを受け取る処理"""
        self.num_items += 1  # 自分のアイテムを増やす
        print(f" -> {self.name}: {from_char.name}から薬草を受け取りました！ (合計: {self.num_items})")


class Main():
    def __init__(self):
        # 1. 各キャラクターの初期の薬草数だけをリストで定義
        # （例: 要素が5つなので、Aさん〜Eさんまでの5人が作られます）
        init_items = [5, 0, 2, 0, 0]
        
        self.characters = []
        
        # 2. ループ処理でキャラクターの生成とイベント登録をまとめて行う
        for i, items in enumerate(init_items):
            # アルファベット（A, B, C...）を文字コードから自動生成して名前を付ける
            # 65は文字コードで 'A' を表します（65+0='A', 65+1='B' ...）
            name = f"{chr(65 + i)}さん" 
            
            # インスタンスの作成
            char = Character(name, num_items=items)
            
            # 【重要】自分自身をハンドラーに登録（1行で完結）
            char.push_handlers(char)
            
            # 管理用リストに追加
            self.characters.append(char)

    def run(self):
        print("--- 初期状態 ---")
        self.status_check()

        # リストのインデックス（添え字）を使ってキャラクターを指定します
        # [0]=Aさん, [1]=Bさん, [2]=Cさん, [3]=Dさん, [4]=Eさん
        
        # 0番目（Aさん）から 1番目（Bさん）へ
        self.characters[0].give_item_to(self.characters[1])

        # 2番目（Cさん）から 4番目（Eさん）へ
        self.characters[2].give_item_to(self.characters[4])
        
        # 1番目（Bさん）から 3番目（Dさん）へ
        self.characters[1].give_item_to(self.characters[3])

        print("\n--- 最終状態 ---")
        self.status_check()

    def status_check(self):
        # 状態チェックもリストをループで回すだけなので何人になっても1行です
        for char in self.characters:
            print(f"{char.name}の薬草数 = {char.num_items}")


if __name__ == "__main__":
    main = Main()
    main.run()