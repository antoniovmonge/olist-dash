import pandas as pd
import numpy as np
# from olistdash.utils import haversine_distance
from olistdash.data import Olist

class Order:
    '''
    Data Frames containing all orders delivered as index,
    and various porperties of these orders as columns
    '''

    def __init__(self):
        self.data = Olist().get_data()
        # The constructor of class Order assigns an attribute ".data" to all new instances of Order
        # i.e Order().data is defined

    def get_wait_time(self, is_delivered=True):
            """
            02-01 > Returns a DataFrame with:
            [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
            filtering out non-delivered orders unless specified
            """
            # Hint: Within this instance method, you have access to the instance of the class Order in the variable self
            # make sure we don't create a "view" but a copy
            orders = self.data['orders'].copy()

            # filter delivered orders
            if is_delivered:
                orders = orders.query("order_status=='delivered'").copy()

            # handle datetime
            orders.loc[:, 'order_delivered_customer_date'] = \
                pd.to_datetime(orders['order_delivered_customer_date'])
            orders.loc[:, 'order_estimated_delivery_date'] = \
                pd.to_datetime(orders['order_estimated_delivery_date'])
            orders.loc[:, 'order_purchase_timestamp'] = \
                pd.to_datetime(orders['order_purchase_timestamp'])

            # compute delay vs expected
            orders.loc[:, 'delay_vs_expected'] = \
                (orders['order_estimated_delivery_date'] -
                orders['order_delivered_customer_date']) / np.timedelta64(24, 'h')

            def handle_delay(x):
                # We only want to keep delay where wait_time is longer than expected (not the other way around)
                # This is what drives customer dissatisfaction!
                if x < 0:
                    return abs(x)
                return 0

            orders.loc[:, 'delay_vs_expected'] = \
                orders['delay_vs_expected'].apply(handle_delay)

            # compute wait time
            orders.loc[:, 'wait_time'] = \
                (orders['order_delivered_customer_date'] -
                orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

            # compute expected wait time
            orders.loc[:, 'expected_wait_time'] = \
                (orders['order_estimated_delivery_date'] -
                orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

            return orders[[
                'order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
                'order_status'
            ]]

    def get_review_score(self):
        """
        02-01 > Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        # import data
        reviews = self.data['order_reviews']

        def dim_five_star(d):
            if d == 5:
                return 1
            return 0

        def dim_one_star(d):
            if d == 1:
                return 1
            return 0

        reviews.loc[:, 'dim_is_five_star'] =\
            reviews['review_score'].apply(dim_five_star)

        reviews.loc[:, 'dim_is_one_star'] =\
            reviews['review_score'].apply(dim_one_star)

        return reviews[[
            'order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score'
        ]]
