class OrderBookSimple:

    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def insert_order(self, order_list, order):
        """
        Insert order into a given list (buy/sell) using binary search.
        :param order_list: Buy/sell order list
        :param order: Order to insert
        """
        low, high = 0, len(order_list)
        order_price = order["price"]

        # Binary search
        while low < high:
            mid = (low + high) // 2
            if order_list[mid]["price"] < order_price:
                low = mid + 1
            else:
                high = mid

        order_list.insert(low, order)

    def resolve_potential_matches(self):
        """
        Check if there is a potential buy/sell match and resolve it.
        :returns True if there is a match
        """
        if len(self.sell_orders) == 0 or len(self.buy_orders) == 0:
            return False

        # If there is a match, resolve the order
        if self.buy_orders[-1]["price"] >= self.sell_orders[0]["price"]:
            lowest_sell_order = self.sell_orders.pop(0)
            highest_buy_order = self.buy_orders.pop()

            print(
                f"Match order: {lowest_sell_order['id']} and {highest_buy_order['id']} at {lowest_sell_order['price']} for ",
                end='')
            if highest_buy_order["quantity"] == lowest_sell_order["quantity"]:
                print(highest_buy_order["quantity"])
                # If it's the same quantity, it is resolved, don't return the orders back to the list.
                pass
            elif highest_buy_order["quantity"] > lowest_sell_order["quantity"]:
                print(lowest_sell_order["quantity"])
                # If there were more buy orders, mutate the quantity and return it to the list
                highest_buy_order["quantity"] -= lowest_sell_order["quantity"]
                self.insert_order(self.buy_orders, highest_buy_order)
            else:
                print(highest_buy_order["quantity"])
                # If there were more sell orders, mutate the quantity and return it to the list
                lowest_sell_order["quantity"] -= highest_buy_order["quantity"]
                self.insert_order(self.sell_orders, lowest_sell_order)
            return True
        return False

    def process_order(self, order):
        """
        Process one order
        """
        # First insert order into the orderbook
        if order["type"] == "buy":
            self.insert_order(self.buy_orders, order)
        else:
            self.insert_order(self.sell_orders, order)

        # After adding an order, check if there is a match
        self.resolve_potential_matches()

    def process_order_list(self, order_list):
        for order in order_list:
            self.process_order(order)

if __name__ == "__main__":
    orderbook = OrderBookSimple()

    incoming_orders = [
        {"id": 1, "type": "buy", "price": 100, "quantity": 10},
        {"id": 2, "type": "sell", "price": 105, "quantity": 5},
        {"id": 3, "type": "buy", "price": 102, "quantity": 8},
        {"id": 4, "type": "sell", "price": 101, "quantity": 10},
        {"id": 5, "type": "buy", "price": 101, "quantity": 5},
        {"id": 6, "type": "sell", "price": 100, "quantity": 3},
    ]

    orderbook.process_order_list(incoming_orders)
