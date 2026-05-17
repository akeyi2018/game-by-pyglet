from pyglet.event import EventDispatcher

class CharacterA(EventDispatcher):
    def __init__(self, num_items=5):
        super().__init__() # EventDispatcherの初期化を呼び出す
        self.register_event_type('on_give_item') # カスタムイベントの登録
        self.num_items = num_items

    def on_give_item(self):
        print("CharacterA: Aさんが薬草を渡しました")
        self.num_items -= 1  # Aさんの薬草数を減らす

class CharacterB(EventDispatcher):
    def __init__(self, num_items=0):
        super().__init__() # EventDispatcherの初期化を呼び出す
        self.register_event_type('on_receive_item') # カスタムイベントの登録
        self.num_items = num_items    # Bさんが持っている薬草の数

    def on_give_item(self):
        self.receive_item()  # Aさんからアイテムを受け取る処理を呼び出す

    def receive_item(self):
    #     print("CharacterBがアイテムを受け取りました")
        self.dispatch_event('on_receive_item') # イベントの発火

    def on_receive_item(self):
        print("CharacterB: Aさんから薬草を受け取りました")
        self.num_items += 1  # Bさんの薬草数を増やす


class Main():
    def __init__(self):
        self.characterA = CharacterA()
        self.characterB = CharacterB()
        # CharacterAのイベントをCharacterBがリッスン
        self.characterA.push_handlers(self.characterB)
        # CharacterBのイベントをCharacterAがリッスン
        self.characterB.push_handlers(self.characterA)


    def run(self):
        
        print(f"初期状態: Aの薬草数 = {self.characterA.num_items}, Bの薬草数 = {self.characterB.num_items}")
        # AがBにアイテムを渡す
        self.characterA.dispatch_event('on_give_item') # Aさんが薬草を渡すイベントを発火

        print(f"最終状態: Aの薬草数 = {self.characterA.num_items}, Bの薬草数 = {self.characterB.num_items}")


if __name__ == "__main__":
    main = Main()
    main.run()