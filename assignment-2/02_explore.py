import altair as alt
import pandas as pd

df = pd.read_csv("data/processed/survey_clean.csv")
df["date"] = pd.to_datetime(df["date"])

freq_order = ["First Time", "Occasionally", "Regularly"]
age_order = ["18-24", "25-34", "35-44", "45-54", "55+"]
status_order = ["Tried at least one", "Heard of them, haven't tried", "Haven't heard of them"]

# 1. responses per day
per_day = df.groupby("date").size().reset_index(name="responses")
chart1 = alt.Chart(per_day).mark_bar().encode(
    x=alt.X("date:T", title="Date submitted"),
    y=alt.Y("responses:Q", title="Responses that day"),
).properties(width=500, height=200, title="Responses per day")
chart1.save("figures/explore_1_responses_per_day.png", scale_factor=2)

# 2. satisfaction counts
chart2 = alt.Chart(df).mark_bar().encode(
    x=alt.X("satisfaction:O", title="Overall satisfaction (1-5)",
            scale=alt.Scale(domain=[1, 2, 3, 4, 5]), axis=alt.Axis(labelAngle=0)),
    y=alt.Y("count()", title="Number of responses"),
).properties(width=300, height=200, title="Overall satisfaction")
chart2.save("figures/explore_2_satisfaction_counts.png", scale_factor=2)

# 3. visit frequency by new items
cell_counts = df.groupby(["visit_freq", "new_items_status"]).size().reset_index(name="n")
boxes = alt.Chart(cell_counts).mark_rect().encode(
    x=alt.X("new_items_status:N", sort=status_order, title=None, axis=alt.Axis(labelAngle=-30)),
    y=alt.Y("visit_freq:N", sort=freq_order, title="Visit frequency"),
    color=alt.Color("n:Q", title="Responses"),
).properties(width=300, height=150, title="Visit frequency x new items (counts)")
numbers = alt.Chart(cell_counts).mark_text().encode(
    x=alt.X("new_items_status:N", sort=status_order),
    y=alt.Y("visit_freq:N", sort=freq_order),
    text="n:Q",
    color=alt.condition(alt.datum.n > 3, alt.value("white"), alt.value("black")),
)
(boxes + numbers).save("figures/explore_3_frequency_by_new_items.png", scale_factor=2)

# 4. age range by order
chart4 = alt.Chart(df).mark_bar().encode(
    x=alt.X("age_range:N", sort=age_order, title="Age range"),
    y=alt.Y("count()", title="Responses"),
    color=alt.Color("order_group:N", title="Order"),
).properties(width=300, height=200, title="Age range x what was ordered")
chart4.save("figures/explore_4_age_by_order.png", scale_factor=2)

# numbers i used in the writeup
print("tried at least one:", (df["new_items_status"] == "Tried at least one").sum(), "of", len(df))
print(df[df["visit_freq"] == "Regularly"]["new_items_status"].value_counts())
print(df.groupby("location")["satisfaction"].agg(["count", "mean"]).round(2))
