import pandas as pd

df = pd.read_csv("data/original/survey-responses-a2.csv")

# shorter column names
df.columns = ["timestamp", "location", "satisfaction", "food", "service", "atmosphere",
              "order_text", "visit_freq", "new_items_raw", "age_range", "comment"]

# dates
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour

# fill blanks
df["location"] = df["location"].fillna("Unknown")
df["order_text"] = df["order_text"].fillna("")
df["comment"] = df["comment"].fillna("")

# put categories in order
df["visit_freq"] = pd.Categorical(df["visit_freq"], ["First Time", "Occasionally", "Regularly"], ordered=True)
df["age_range"] = pd.Categorical(df["age_range"], ["18-24", "25-34", "35-44", "45-54", "55+"], ordered=True)

# new items question: one true/false column per answer
df["tried_calzones"] = df["new_items_raw"].str.contains("Calzones")
df["tried_deep_dish"] = df["new_items_raw"].str.contains("Caramelized Deep Dish")
df["tried_popcorn"] = df["new_items_raw"].str.contains("Gourmet Popcorn")
df["not_tried_any"] = df["new_items_raw"].str.contains("Haven't tried any")
df["not_heard"] = df["new_items_raw"].str.contains("Haven't heard of them")

df["n_items_tried"] = df["tried_calzones"].astype(int) + df["tried_deep_dish"].astype(int) + df["tried_popcorn"].astype(int)

# one column with 3 groups
# if someone checked both "haven't tried" and "haven't heard", they go in "haven't heard"
status = []
for i in range(len(df)):
    if df["n_items_tried"][i] > 0:
        status.append("Tried at least one")
    elif df["not_heard"][i]:
        status.append("Haven't heard of them")
    else:
        status.append("Heard of them, haven't tried")
df["new_items_status"] = status

# orders were typed in, so look for keywords
text = df["order_text"].str.lower()
df["ordered_pizza"] = text.str.contains("pizza|slice|deep dish|deepdish|sausage|pepperoni")
df["ordered_wings"] = text.str.contains("wing")
df["ordered_salad"] = text.str.contains("salad")
df["ordered_other"] = text.str.contains("appetizer|hamburger|fries|spaghetti")

# some answers say nothing about food ("nothing", "Delivery", blank)
any_food = df["ordered_pizza"] | df["ordered_wings"] | df["ordered_salad"] | df["ordered_other"]
df["order_unclear"] = ~any_food

# simpler order groups for charts
more_than_pizza = df["ordered_wings"] | df["ordered_salad"] | df["ordered_other"]
order_group = []
for i in range(len(df)):
    if df["order_unclear"][i]:
        order_group.append("Unclear")
    elif df["ordered_pizza"][i] and more_than_pizza[i]:
        order_group.append("Pizza + something else")
    elif df["ordered_pizza"][i]:
        order_group.append("Pizza only")
    else:
        order_group.append("No pizza")
df["order_group"] = order_group

# comments that talk about price
df["mentions_price"] = df["comment"].str.lower().str.contains("pric|expens|afford|deal|competitive")

# add an id and save
df.insert(0, "response_id", range(1, len(df) + 1))
df.to_csv("data/processed/survey_clean.csv", index=False)

print(len(df), "rows saved")
print(df["new_items_status"].value_counts())
print(df["order_group"].value_counts())
