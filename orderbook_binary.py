from sortedcontainers import SortedDict
from enum import Enum

from util import DoublyLinkedList


class QueryType(Enum):
    ADD_ORDER = 1
    CANCEL_ORDER = 2
    MODIFY_ORDER = 3

class OrderType(Enum):
    BUY = 1
    SELL = 2

class Query:
    pass

class Cancel(Query):
    def __init__(self, order_id):
        self.order_id = order_id

class Order(Query):

    def __init__(self, price, quantity, order_id, order_type):
        self.price = price
        self.quantity = quantity
        self.order_id = order_id
        self.order_type = order_type

class OrderBookBinary:

    def __init__(self):
        self.buy_orders = SortedDict()
        self.sell_orders = SortedDict()

        self.order_map = dict()

    def insert_order(self, order_list, order):
        """
        Insert order into a given list (buy/sell) using binary search.
        :param order_list: Buy/sell order list
        :param order: Order to insert
        """
        order_node = None
        if order.price not in order_list:
            order_list[order.price] = DoublyLinkedList(order)
            order_node = order_list[order.price].head
        else:
            order_list[order.price].add(order)
            order_node = order_list[order.price].tail

        return order_node

    def remove_order(self, order_id):
        order_node = self.order_map[order_id]
        self.order_map[order_id].remove()
        # If it's the only order in the queue for that level, get rid of the price level
        if order_node.parent_list.size == 0:
            if order_node.value.order_type == OrderType.BUY:
                del self.buy_orders[order_node.value.price]
            if order_node.value.order_type == OrderType.SELL:
                del self.sell_orders[order_node.value.price]
        del self.order_map[order_id]

    def cancel_order(self, cancel_order: Cancel):
        self.remove_order(cancel_order.order_id)

    def resolve_potential_matches(self):
        highest_buy_price, buy_order_queue = self.buy_orders.peekitem(-1) if self.buy_orders else (None, None)
        lowest_sell_price, sell_order_queue = self.sell_orders.peekitem(0) if self.sell_orders else (None, None)

        print(highest_buy_price, "---", lowest_sell_price)
        # If either is None, there is no buy/sell orders so there's nothing to resolve
        if highest_buy_price is None or lowest_sell_price is None:
            return

        # If the highest buy price does not meet the lowest sell price, there's nothing to resolve
        if highest_buy_price < lowest_sell_price:
            return

        # Otherwise we got stuff to resolve
        print("Match!")

        current_buy_order = buy_order_queue.head
        current_sell_order = sell_order_queue.head

        while highest_buy_price >= lowest_sell_price:
            # If the quantities match exactly, both values can be popped from their queues and we're done resolving
            if current_sell_order.value.quantity == current_buy_order.value.quantity:
                self.remove_order(current_buy_order.value.order_id)
                self.remove_order(current_sell_order.value.order_id)
                break
            elif current_sell_order.value.quantity >= current_buy_order.value.quantity:
                current_sell_order.value.quantity -= current_buy_order.value.quantity
                self.remove_order(current_buy_order.value.order_id)
                if buy_order_queue.head is None:
                    highest_buy_price, buy_order_queue = self.buy_orders.peekitem(-1) if self.buy_orders else (None, None)
                if buy_order_queue is None:
                    break
                current_buy_order = buy_order_queue.head
            elif current_buy_order.value.quantity >= current_sell_order.value.quantity:
                current_buy_order.value.quantity -= current_sell_order.value.quantity
                self.remove_order(current_sell_order.value.order_id)
                if sell_order_queue.head is None:
                    lowest_sell_price, sell_order_queue = self.sell_orders.peekitem(0) if self.sell_orders else (None, None)
                if sell_order_queue is None:
                    break
                current_sell_order = sell_order_queue.head
            else:
                raise Exception("Shouldn't happen")

    def process_order(self, order: Order):
        """
        Process one order
        """
        # First insert order into the orderbook
        if order.order_type == OrderType.BUY:
            order_node = self.insert_order(self.buy_orders, order)
            self.order_map[order.order_id] = order_node
        else:
            order_node = self.insert_order(self.sell_orders, order)
            self.order_map[order.order_id] = order_node

        # After adding an order, check if there is a match
        self.resolve_potential_matches()

    def process_queries(self, incoming_queries):
        for query in incoming_queries:
            if isinstance(query, Order):
                self.process_order(query)
            elif isinstance(query, Cancel):
                self.cancel_order(query)
            else:
                raise Exception(f"Invalid query {query}")

    def process_order_list(self, order_list):
        for order in order_list:
            self.process_order(order)

if __name__ == "__main__":
    orderbook = OrderBookBinary()

    incoming_queries = [
        Order(100, 10, 1, OrderType.BUY),
        Order(100, 5, 2, OrderType.BUY),
        Order(100, 5, 3, OrderType.BUY),
        Order(100, 5, 4, OrderType.BUY),
        Order(100, 5, 5, OrderType.BUY),
        Order(90, 100, 6, OrderType.SELL),
    ]

    orderbook.process_queries(incoming_queries)

    print(orderbook)
