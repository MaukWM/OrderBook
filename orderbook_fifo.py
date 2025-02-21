class OrderBookFifo:

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
        new_value = True

        # Binary search
        while low < high:
            mid = (low + high) // 2
            if order_list[mid]["price"] == order_price:
                new_value = False
            if order_list[mid]["price"] < order_price:
                low = mid + 1
            else:
                high = mid

        if new_value:
            order_queue = {
                "price": order["price"],
                "order_queue": [order]
            }
            order_list.insert(low, order_queue)
        else:
            order_list[low]["order_queue"].append(order)

    def resolve_potential_matches(self):
        """
        Check if there is a potential buy/sell match and resolve it.
        :returns True if there is a match
        """
        if len(self.sell_orders) == 0 or len(self.buy_orders) == 0:
            return

        # Retrieve initial queues at respective limit
        lowest_sell_order_queue = self.sell_orders[0]
        highest_buy_order_queue = self.buy_orders[-1]

        while highest_buy_order_queue["price"] >= lowest_sell_order_queue["price"]:
            # Retrieve first-in-line orders. If an order is fully resolved they will be popped from the stack later
            front_sell_order = lowest_sell_order_queue["order_queue"][0]
            front_buy_order = highest_buy_order_queue["order_queue"][0]

            # Keep resolving matches as long they exist
            if front_sell_order["quantity"] == front_buy_order["quantity"]:
                # Remove these orders from their respective queues
                lowest_sell_order_queue["order_queue"].pop(0)
                highest_buy_order_queue["order_queue"].pop(0)
                # If it is exactly the same quantity, we can fully resolve.
                # If the order queue has become empty for this price, remove it.
                if len(lowest_sell_order_queue["order_queue"]) == 0:
                    self.sell_orders.pop(0)
                if len(highest_buy_order_queue["order_queue"]) == 0:
                    self.buy_orders.pop()
                break
            elif front_buy_order["quantity"] > front_sell_order["quantity"]:
                # If there were more buy orders, mutate the quantity and resolve next in line if they exist
                front_buy_order["quantity"] -= front_sell_order["quantity"]
                # First pop the fully resolved order
                lowest_sell_order_queue["order_queue"].pop(0)
                if len(lowest_sell_order_queue["order_queue"]) == 0:
                    self.sell_orders.pop(0)
                    if len(self.sell_orders) == 0:
                        break
                    lowest_sell_order_queue = self.sell_orders[0]
            else:
                # If there were more sell orders, mutate the quantity and return it to the list
                front_sell_order["quantity"] -= front_buy_order["quantity"]
                # First pop the fully resolved order
                highest_buy_order_queue["order_queue"].pop(0)
                if len(highest_buy_order_queue["order_queue"]) == 0:
                    self.buy_orders.pop(-1)
                    if len(self.buy_orders) == 0:
                        break
                    highest_buy_order_queue = self.buy_orders[-1]

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
    orderbook = OrderBookFifo()

    incoming_orders = [
        {"id": 1, "type": "buy", "price": 101, "quantity": 10},
        {"id": 2, "type": "buy", "price": 102, "quantity": 8},
        {"id": 3, "type": "buy", "price": 101, "quantity": 5},
        {"id": 4, "type": "buy", "price": 101, "quantity": 5},
        {"id": 5, "type": "buy", "price": 102, "quantity": 5},
        {"id": 6, "type": "sell", "price": 101, "quantity": 20},
    ]

    orderbook.process_order_list(incoming_orders)

    print(orderbook.buy_orders)
    print(orderbook.sell_orders)
