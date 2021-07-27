import os
import pandas as pd

class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrame loaded from csv files
        """
        #########
        # LOCAL #
        #########
        root_dir = os.path.dirname(os.path.dirname(__file__))
        csv_path = os.path.join(root_dir, "raw_data", "csv")

        # csv_path = ('../raw_data/csv')
        # Create the list file_names
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]

        # Create the list of dict keys
        key_names = [key_name.replace('olist_','').replace('_dataset','').replace('.csv','') for key_name in file_names]

        # Create the dictionary
        data = {}
        for k,f in zip(key_names, file_names):
            data[k] = pd.read_csv(os.path.join(csv_path, f))
        return data

        ###################
        # AWS S3 - beging #
        ###################

        # file_paths = [
        #     's3://olistdashdb/csv/olist_sellers_dataset.csv',
        #     's3://olistdashdb/csv/olist_order_reviews_dataset.csv',
        #     's3://olistdashdb/csv/olist_order_items_dataset.csv',
        #     's3://olistdashdb/csv/olist_customers_dataset.csv',
        #     's3://olistdashdb/csv/olist_orders_dataset.csv',
        #     's3://olistdashdb/csv/olist_order_payments_dataset.csv',
        #     's3://olistdashdb/csv/product_category_name_translation.csv',
        #     's3://olistdashdb/csv/product_category_name_translation.csv',
        #     's3://olistdashdb/csv/product_category_name_translation.csv']

        # key_names = [
        #     'sellers',
        #     'order_reviews',
        #     'order_items',
        #     'customers',
        #     'orders',
        #     'order_payments',
        #     'product_category_name_translation',
        #     'products',
        #     'geolocation']

        # data = {}
        # for k,f in zip(key_names, file_paths):
        #     data[k] = pd.read_csv(f)
        # return data

        ################
        # AWS S3 - end #
        ################

    def get_matching_table(self):
        """
        This function returns a matching table between
        columns [ "order_id", "review_id", "customer_id", "product_id", "seller_id"]
        """

        data = self.get_data()

        # Selecting columns of interest
        orders = data['orders'][['customer_id', 'order_id']]
        reviews = data['order_reviews'][['order_id', 'review_id']]
        items = data['order_items'][['order_id', 'product_id', 'seller_id']]

        # Merge DataFrame
        matching_table = orders\
            .merge(reviews, on='order_id', how='outer')\
            .merge(items, on='order_id', how='outer')

        return matching_table
