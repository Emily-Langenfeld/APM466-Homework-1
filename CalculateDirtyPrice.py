from datetime import datetime

# Since all the bonds we are working with mature exactly 6 months apart from each other,
# the last coupon payment occurred on the same day. The next bond will mature on March 1st, 2025.
# Since the bonds pay the coupons biannually, the last coupon payment must have occurred on
# September 1st, 2024.


def calculate_dirty_price(df):
    last_coupon = datetime(2024, 9, 1)
    df["LAST COUPON"] = (df["DATE"] - last_coupon).dt.days
    df["DIRTY PRICE"] = df["PRICE"] + ((df["LAST COUPON"]/365)*df["COUPON"])

    return df
