import altair as alt
import pandas as pd

df = pd.read_csv("data/processed/survey_clean.csv")

freq_order = ["First Time", "Occasionally", "Regularly"]
status_order = ["Tried at least one", "Heard of them, haven't tried", "Haven't heard of them"]


# v2: one bar per visit frequency, split into the 3 groups
# each bar goes from 0% to 100% of that row, with the count written inside
rows = []
row_labels = []
for freq in freq_order:
    group = df[df["visit_freq"] == freq]
    label = freq + " (n=" + str(len(group)) + ")"
    row_labels.append(label)
    start = 0
    for status in status_order:
        count = int((group["new_items_status"] == status).sum())
        share = count / len(group)
        rows.append({"row": label, "status": status, "count": count,
                     "start": start, "end": start + share, "middle": start + share / 2})
        start = start + share
bars_df = pd.DataFrame(rows)

colors = alt.Scale(domain=status_order, range=["#08519c", "#6baed6", "#fdae6b"])

bars = alt.Chart(bars_df).mark_bar(stroke="white").encode(
    x=alt.X("start:Q", title="share of people in that group", axis=alt.Axis(format="%")),
    x2="end:Q",
    y=alt.Y("row:N", sort=row_labels, title=None),
    color=alt.Color("status:N", scale=colors, sort=status_order, title="new items"),
).properties(width=520, height=200, title="Have visitors tried the new items?")

numbers = alt.Chart(bars_df[bars_df["count"] > 0]).mark_text(fontSize=16).encode(
    x="middle:Q",
    y=alt.Y("row:N", sort=row_labels),
    text="count:Q",
    color=alt.condition(alt.datum.status == "Tried at least one", alt.value("white"), alt.value("black")),
)
(bars + numbers).save("figures/direction1_v2_stacked_bars.png", scale_factor=2)

print("saved v2")


# v3: add a small chart of which items were tried
# v2 lost the per-item detail, so it comes back as its own chart
items = pd.DataFrame({"item": ["Calzones", "Caramelized Deep Dish", "Gourmet Popcorn"],
                      "count": [int(df["tried_calzones"].sum()),
                                int(df["tried_deep_dish"].sum()),
                                int(df["tried_popcorn"].sum())]})
item_bars = alt.Chart(items).mark_bar(color="#08519c").encode(
    x=alt.X("count:Q", title="people who tried it", axis=alt.Axis(tickMinStep=1), scale=alt.Scale(domain=[0, 6])),
    y=alt.Y("item:N", sort=None, title=None),
).properties(width=200, height=120, title="Which items were tried?")
item_numbers = item_bars.mark_text(align="left", dx=4, fontSize=14).encode(text="count:Q")

left = (bars + numbers).properties(width=380)
alt.hconcat(left, item_bars + item_numbers).resolve_scale(color="independent").save(
    "figures/direction1_v3_item_bars.png", scale_factor=2)

print("saved v3")
