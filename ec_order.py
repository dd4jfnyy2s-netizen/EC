# EC注文管理アプリ
import json

class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
# 表示関数
    def show_info(self):
        print(f"商品名: {self.name}")
        print(f"価格: {self.price}円")
        print(f"在庫: {self.stock}個")
# 追加関数
    def add_stock(self,amount):
        if amount < 1:
            print("1以上の数字を入力してください")
            return
        self.stock += amount
# 販売関数
    def sell(self, amount):
        if amount < 1:
            print("1以上の数字を入力してください")
            return
        if amount > self.stock:
            print("在庫が足りません")
            return
        self.stock -= amount
        total_price = self.price * amount
        return total_price

class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product, amount):
        found = False
        if amount < 1:
            print("1以上の数字を入力してください")
            return
        if amount > product.stock:
            print("在庫が足りません")
            return
        for item in self.items:
            if item["product"] == product:
                if item["amount"] + amount > product.stock:
                    print("在庫が足りません")
                    return
                found = True
                item["amount"] = item["amount"] + amount
        if not found :
            self.items.append({
                "product": product,
                "amount": amount
            })

    def show_cart(self):
        if not self.items:
            print("カートの中身が空です")
            return         
        for item in self.items:
            print(f"{item['product'].name} × {item['amount']}個")

    def get_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item["product"].price * item["amount"]
        return total_price

    def delete_product(self):
        if not self.items:
            print("カートの中身が空です")
            return
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item['product'].name} × {item['amount']}")
        try:
            delete_number = int(input("削除する商品番号: "))
            if delete_number < 1 or delete_number > len(self.items):
                print("数字を正しく入力してください")
                return
        except ValueError:
            print("数字で入力してください")
            return
        index = delete_number - 1
        self.items.pop(index)

    def change_amount(self):
        if not self.items:
            print("カートの中身が空です")
            return
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item['product'].name} × {item['amount']}")
        try:
            change_number = int(input("変更する商品番号: "))
            if change_number < 1 or change_number > len(self.items):
                print("数字を正しく入力してください")
                return
        except ValueError:
            print("数字で入力してください")
            return
        try:
            change_amount = int(input("新しい数量: "))
            if change_amount < 1:
                print("1以上の数字を入力してください")
                return
        except ValueError:
            print("数字で入力してください")
            return
        index = change_number - 1

        if change_amount > self.items[index]["product"].stock:
            print("在庫がありません")
            return

        self.items[index]["amount"] = change_amount
        
class Order:
    def __init__(self, cart):
        self.cart = cart
        self.order_history = []
        self.next_order_id = 1

    def confirm_order(self):
        if not self.cart.items:
            print("カートの中身が空です")
            return
        for item in self.cart.items:
            if item["amount"] > item["product"].stock:
                print(f"{item['product'].name}の在庫が足りません")
                return
        total_price = 0       
        for item in self.cart.items:
            print(f"商品名: {item['product'].name}")
            print(f"数量: {item['amount']}")
            item["product"].sell(item["amount"])
            total_price += item['product'].price * item['amount']
        order_data = {
            "order_id": self.next_order_id,
            "items": self.cart.items.copy(),
            "total_price": total_price
        }
        self.order_history.append(order_data)
        self.next_order_id += 1
        self.cart.items.clear()

    def sell_log(self):
        if not self.order_history:
            print("注文履歴がありません")
            return
        print("== 注文履歴 ==")
        for history in self.order_history:
            print(f"注文番号: {history['order_id']}")
            for item in history['items']:
                print(f"商品名: {item['product'].name}")
                print(f"数量: {item['amount']}")
            print(f"合計金額: {history['total_price']}円")

    def find_order(self):
        found = False
        try:
            find_number = int(input("注文番号: "))
            if find_number < 1:
                print("注文番号を1以上で入力してください")
                return
        except ValueError:
            print("数字で入力してください")
            return        
        for history in self.order_history:
            if find_number == history['order_id']:
                found = True
                print(f"== 注文{history['order_id']} ==")
                for item in history['items']:
                    print(f"商品名: {item['product'].name}")
                    print(f"数量: {item['amount']}")
                print(f"合計金額: {history['total_price']}円")
        if not found:
            print("該当する注文番号が見つかりません")
            return

    def cancel_order(self):
        try:
            cancel_number = int(input("注文番号: "))
            if cancel_number < 1:
                print("注文番号を1以上で入力してください")
                return
        except ValueError:
            print("数字で入力してください")
            return
        found = False
        for history in self.order_history:
            if cancel_number == history["order_id"]:
                found = True
                print(f"注文{history['order_id']}をキャンセルしますか？")
                selects = ["はい", "いいえ"]
                for i, select in enumerate(selects, start=1):
                    print(f"{i}. {select}")
                try:
                    choice = int(input("数字を入力してください"))
                except ValueError:
                    print("数字を入力してください")
                    return
                if choice == 1:
                    for item in history["items"]:
                        item["product"].add_stock(item["amount"])
                    self.order_history.remove(history)
                    print("注文をキャンセルしました")
                    return
                elif choice == 2:
                    print("キャンセルを取りやめました")
                    return
                else:
                    print("1か2を入力してください")
                    return
        if not found:
            print("該当する注文番号が見つかりません")
            return

def load_product():
    try:
        with open("ec_order.json", "r", encoding="utf-8") as f:
            product_data = json.load(f)

            products = []

            for data in product_data:
                product = Product(
                    data["name"],
                    data["price"],
                    data["stock"]
                )
                products.append(product)
            return products
    except FileNotFoundError:
        return []

def load_order_history():
    try:
        with open("order_history.json", "r", encoding="utf-8") as f:
            history_data = json.load(f)

            order_history = []

            for history in history_data:
                items_data = []
                for item in history["items"]:
                    for product in products:
                        if product.name == item["name"]:
                            items_data.append({
                                "product": product,
                                "amount": item["amount"]
                            })
                order_history.append({
                    "order_id": history["order_id"],
                    "items": items_data,
                    "total_price": history["total_price"]
                })
            return order_history
    except FileNotFoundError:
        return []

products = load_product()

def save_product():
    product_data = []

    for product in products:
        product_data.append({
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })

    with open("ec_order.json", "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)

def save_order_history():
    history_data = []

    for history in order.order_history:

        items_data = []

        for item in history["items"]:
            items_data.append({
                "name": item["product"].name,
                "amount": item["amount"]
            })

        history_data.append({
            "order_id": history["order_id"],
            "items": items_data,
            "total_price": history["total_price"]
        })
    with open("order_history.json", "w", encoding="utf-8") as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

def judge():
    try:
        choice = int(input("商品番号を入力してください: "))
        if choice < 1 or choice > len(products):
            print("数字を正しく入力してください")
            return
    except ValueError:
        print("数字で入力してください")
        return
    return choice

if not products:
    product1 = Product("りんご", 150, 10)
    product2 = Product("バナナ", 120, 20)
    products = [product1, product2]

cart = Cart()
order = Order(cart)
order.order_history = load_order_history()

if order.order_history:
    order.next_order_id = max(history["order_id"] for history in order.order_history) + 1
else:
    order.next_order_id = 1

menus = ["カートに追加", "商品一覧", "商品を入庫", "カートを見る", "カートの数量を変更", "カートから削除", "注文確定", "注文履歴", "注文検索", "注文をキャンセル", "終了"]

while True:
    for i, menu in enumerate(menus, start=1):
        print(f"{i}. {menu}")
    try:
        action = int(input("操作を選択してください: "))
        if action < 1 or action > 11:
            print("数字を正しく入力してください")
            continue
    except ValueError:
        print("数字で入力してください")
        continue

    if action == 1:    
        print("=== 商品一覧 ===")
        choice = judge()
        if choice is None:
            continue
        try:
            amount = int(input("数量: "))
            if amount < 1:
                print("1以上の数字を入力してください")
                continue
        except ValueError:
            print("数字で入力してください")
            continue

        selected_product = products[choice - 1]
        cart.add_product(selected_product, amount)
        print("== カート ==")
        cart.show_cart()
    elif action == 2:
        for product in products:
            product.show_info()
    elif action == 3:
        print("=== 商品の入庫 ===")
        for i, product in enumerate(products, start=1):
            print(f"{i}. {product.name}")
        choice = judge()
        if choice is None:
            continue
        try:
            amount = int(input("入庫する数量: "))
            if amount <= 0:
                print("入庫する数量を1以上で入力してください")
                continue
        except ValueError:
            print("数字で入力してください")
            continue 
        selected_product = products[choice - 1]
        selected_product.add_stock(amount)
    elif action == 4:
        print("== カート ==")
        cart.show_cart()
    elif action == 5:
        print("== カート ==")
        cart.change_amount()
    elif action == 6:
        print("== カート ==")
        cart.delete_product()
    elif action == 7:
        cart.show_cart()
        print("注文を確定します")
        order.confirm_order()
    elif action == 8:
        order.sell_log()
    elif action == 9:
        order.find_order()
    elif action == 10:
        order.cancel_order()    
    elif action == 11:
        print("アプリを終了します")
        save_product()
        save_order_history()
        break