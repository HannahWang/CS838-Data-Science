import pandas as pd

E = pd.read_csv("E.csv")


price_cols = ['price_yelp', 'price_trip']
rating_cols = ['rating_yelp', 'rating_trip']
review_cols = ['review_count_yelp', 'review_count_trip']
E['price'] = E.loc[:,price_cols].mean(1)
E['rating'] = E.loc[:,rating_cols].mean(1)
E['review_count'] = E.loc[:,review_cols].sum(1)
E = E.drop(columns = price_cols)
E = E.drop(columns = rating_cols)
E = E.drop(columns = review_cols)

print(list(E))

E.to_csv('E_merge.csv', index=False)
