import pandas as pd
import numpy as np
from olistdash.data import Olist
from olistdash.order import Order

class Seller:

    def __init__(self):
        # Import data only once
        olist = Olist()
        self.data = olist.get_data()
        self.matching_table = olist.get_matching_table()
        self.order = Order()

    def get_seller_features(self):
        """
        Returns a DataFrame with:
        'seller_id','seller_city', 'seller_state'
        """
        # Making a copy before using inplace=True to avoid modifying
        # self.data
        sellers = self.data['sellers'].copy()
        sellers.drop('seller_zip_code_prefix', axis=1, inplace=True)
        # There are multiple rows per seller
        sellers.drop_duplicates(inplace=True)
        return sellers

    def get_seller_delay_wait_time(self):
        """
        Returns a DataFrame with:
        'seller_id', 'delay_to_carrier', 'seller_state'
        """
        # Get data
        order_items = self.data['order_items'].copy()
        orders = self.data['orders'].query("order_status=='delivered'").copy()

        ship = order_items.merge(orders, on='order_id')

        # Handling datetime
        ship.loc[:, 'shipping_limit_date'] = pd.to_datetime(
            ship['shipping_limit_date'])
        ship.loc[:, 'order_delivered_carrier_date'] = pd.to_datetime(
            ship['order_delivered_carrier_date'])
        ship.loc[:, 'order_delivered_customer_date'] = pd.to_datetime(
            ship['order_delivered_customer_date'])
        ship.loc[:, 'order_purchase_timestamp'] = pd.to_datetime(
            ship['order_purchase_timestamp'])

        # Computing delay and wait_time
        def handle_early_dropoff(x):
            if x < 0:
                return abs(x)
            return 0

        def delay_to_logistic_partner(df):
            df['delay'] = (
                df.shipping_limit_date - 
                df.order_delivered_carrier_date) / np.timedelta64(24, 'h')
            df.loc[:,'delay'] = df.delay.apply(handle_early_dropoff)
            return np.mean(df.delay)

        def order_wait_time(df):
            days = np.mean(
                (df.order_delivered_customer_date - df.order_purchase_timestamp)
                / np.timedelta64(24, 'h')
            )
            return days

        delay = ship\
            .groupby('seller_id')\
                .apply(delay_to_logistic_partner)\
                    .reset_index()

        delay.columns = ['seller_id', 'delay_to_carrier']

        wait = ship\
            .groupby('seller_id')\
                .apply(order_wait_time)\
                    .reset_index()
        wait.columns = ['seller_id', 'wait_time']

        order_wait_time_df = delay.merge(wait, on='seller_id')

        return order_wait_time_df

        
