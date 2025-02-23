from matplotlib import pyplot as plt

from orderbook_binary import OrderBookBinary

def count_volume(linked_list):
    current = linked_list.head
    total = 0
    while current:
        total += current.value.quantity
        current = current.next
    return total

def retrieve_depth_data(orderbook: OrderBookBinary):
    bid_prices, bid_cumulative = [], []
    ask_prices, ask_cumulative = [], []

    for price, linked_list in reversed(orderbook.buy_orders.items()):
        cumulative_volume = count_volume(linked_list)
        bid_prices.append(price)
        bid_cumulative.append(cumulative_volume)

    for price, linked_list in orderbook.sell_orders.items():
        cumulative_volume = count_volume(linked_list)
        ask_prices.append(price)
        ask_cumulative.append(cumulative_volume)

    return bid_prices, bid_cumulative, ask_prices, ask_cumulative


def plot_orderbook_depth(orderbook: OrderBookBinary):
    bid_prices, bid_cumulative, ask_prices, ask_cumulative = retrieve_depth_data(orderbook)

    plt.figure(figsize=(10, 5))
    plt.step(bid_prices[::-1], bid_cumulative, label="Bids (Buy Orders)", color="green", where="post")
    plt.step(ask_prices, ask_cumulative, label="Asks (Sell Orders)", color="red", where="post")

    plt.xlabel("Price")
    plt.ylabel("Cumulative Volume")
    plt.title("Order Book Depth Chart")
    plt.legend()
    plt.grid()
    plt.show()