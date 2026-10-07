"""Logic copied from Assignment1-Zheyu Wang.ipynb (Rosa's Pizza)."""

import numpy as np
from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times


def best_promise_time(zones, time_blocks, promise_B, costs):
    """Try each promise in promise_B and return (best promise, its profit)."""
    profits = []
    for p in promise_B:
        array = delivery_times(zones, time_blocks, p)
        late_order = np.sum(array > p)
        total_order = len(array)

        # profit from all orders minus the cost of each late order
        order_profit = total_order * costs['margin'] - late_order * (costs["refund"] + costs["churn_orders"] * costs["margin"])
        profits.append(order_profit)
    best_index = np.argmax(profits)
    return promise_B[best_index], profits[best_index]
