from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv

engine = create_engine('sqlite:///data.sqlite')
create_table_from_csv(engine,
                      "E_merge.csv",
                      table_name="restaurants",
                      fields=[
                            ("id", "integer"),
                            ("name", "string"),
                            ("city", "string"),
                            ("zipcode", "string"),
                            ("address", "string"),
                            ("phone", "string"),
                            ("category", "string"),
                            ("category_loc", "string"),
                            ("category_food", "string"),
                            ("price", "float"),
                            ("rating", "float"),
                            ("review_count", "integer"),
                            ("hours_sun_open", "string"),
                            ("hours_sun_close", "string"),
                            ("hours_mon_open", "string"),
                            ("hours_mon_close", "string"),
                            ("hours_tue_open", "string"),
                            ("hours_tue_close", "string"),
                            ("hours_wed_open", "string"),
                            ("hours_wed_close", "string"),
                            ("hours_thu_open", "string"),
                            ("hours_thu_close", "string"),
                            ("hours_fri_open", "string"),
                            ("hours_fri_close", "string"),
                            ("hours_sat_open", "string"),
                            ("hours_sat_close", "string")],
                      create_id = False
                     )

from cubes import Workspace
from cubes import PointCut
from cubes import Cell

from prettytable import PrettyTable

workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///data.sqlite")
workspace.import_model("model.json")
browser = workspace.browser("restaurants")
cube = workspace.cube("restaurants")

'''
# aggregation by zipcode
print("ZipCode, # Restaurants")
result = browser.aggregate(drilldown=["location:zipcode"])
for record in result:
    print(record['location.zipcode'], ",", record['num_restaurants'])
print()
'''

# aggregation by restaurant price
result = browser.aggregate(drilldown=["price"])
t = PrettyTable(['Price', '# Restaurants', 'Avg. Rating', '# Reviews/Restaurant', 'Avg. Sun. Open Hours', 'Avg. Sun. Close Hours', 'Avg. Mon. Open Hours', 'Avg. Mon. Close Hours'])
for record in result:
    t.add_row([round(record['price'],3), record['num_restaurants'], round(record['rating_avg'],3), round(record['review_count_sum']/record['num_restaurants']), round(record['hours_sun_open_avg']), round(record['hours_sun_close_avg']), round(record['hours_mon_open_avg']), round(record['hours_mon_close_avg'])])
print(t)
print()

# aggregation by restaurant rating
result = browser.aggregate(drilldown=["review:rating"])
t = PrettyTable(['Rating', '# Restaurants', 'Avg. Price', '# Reviews/Restaurant', 'Avg. Sun. Open Hours', 'Avg. Sun. Close Hours', 'Avg. Mon. Open Hours', 'Avg. Mon. Close Hours'])
for record in result:
    t.add_row([round(record['review.rating'],3), record['num_restaurants'], round(record['price_avg'],3), round(record['review_count_sum']/record['num_restaurants']), round(record['hours_sun_open_avg']), round(record['hours_sun_close_avg']), round(record['hours_mon_open_avg']), round(record['hours_mon_close_avg'])])
print(t)
print()

# aggregation by category location
result = browser.aggregate(drilldown=["category_loc"])
t = PrettyTable(['Cat:Location', '# Restaurants', 'Avg. Price', 'Avg. Rating', '# Reviews/Restaurant', 'Sun. Open Hours', 'Sun. Close Hours', 'Mon. Open Hours', 'Mon. Close Hours'])
for record in result:
    t.add_row([record['category_loc'], record['num_restaurants'], round(record['price_avg'],3), round(record['rating_avg'],3), round(record['review_count_sum']/record['num_restaurants']), round(record['hours_sun_open_avg']), round(record['hours_sun_close_avg']), round(record['hours_mon_open_avg']), round(record['hours_mon_close_avg'])])
print(t)
print()


# aggregation by category food
result = browser.aggregate(drilldown=["category_food"])
t = PrettyTable(['Cat:Food', '# Restaurants', 'Avg. Price', 'Avg. Rating', '# Reviews/Restaurant', 'Sun. Open Hours', 'Sun. Close Hours', 'Mon. Open Hours', 'Mon. Close Hours'])
for record in result:
    t.add_row([record['category_food'], record['num_restaurants'], round(record['price_avg'],3), round(record['rating_avg'],3), round(record['review_count_sum']/record['num_restaurants']), round(record['hours_sun_open_avg']), round(record['hours_sun_close_avg']), round(record['hours_mon_open_avg']), round(record['hours_mon_close_avg'])])
print(t)
print()

