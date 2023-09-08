import pandas as pd
import re

# read unformatted_products.csv
product_df = pd.read_csv("WhiteCap/products.csv")
# iterate through productid column
for index, row in product_df.iterrows():
    # remove first 3 numbers from product id
    product_df.at[index, "Product_ID"] = re.sub(r"^\d{3}", "", row["Product_ID"])

    # remove dollar sign from price
    product_df.at[index, "Price"] = re.sub(r"[$]", "", row["Price"])

    # remove whitespace from price
    product_df.at[index, "Price"] = re.sub(r"\s", "", row["Price"])

    # remove irrelevant products that match with a python regex
    if re.search(r"^(?!.*([LH]US|HGUS)\d).*$", row["Product_ID"]) != None:
        product_df.drop(index, inplace=True)

# save to new csv file
product_df.to_csv("WhiteCap/products.csv", index=False)
