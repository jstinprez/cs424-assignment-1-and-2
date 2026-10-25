import altair as alt
import pandas as pd

df = pd.read_csv("data/processed/survey_clean.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

freq_order = ["First Time", "Occasionally", "Regularly"]
age_order = ["18-24", "25-34", "35-44", "45-54", "55+"]


# direction 1: visit frequency by new items, shaded by share of each row
columns = {
    "Calzones": df["tried_calzones"],
    "Caramelized Deep Dish": df["tried_deep_dish"],
    "Gourmet Popcorn": df["tried_popcorn"],
    "Heard of, not tried": df["new_items_status"] == "Heard of them, haven't tried",
    "Never heard of": df["new_items_status"] == "Haven't heard of them",
}
rows = []
row_labels = []
for freq in freq_order:
    group = df[df["visit_freq"] == freq]
    label = freq + " (n=" + str(len(group)) + ")"
    row_labels.append(label)
    for name, flag in columns.items():
        count = int(flag[group.index].sum())
        rows.append({"row": label, "column": name, "count": count, "share": count / len(group)})
grid = pd.DataFrame(rows)

col_order = list(columns.keys())
boxes = alt.Chart(grid).mark_rect(stroke="white").encode(
    x=alt.X("column:N", sort=col_order, title=None, axis=alt.Axis(orient="top", labelAngle=0, labelLimit=120)),
    y=alt.Y("row:N", sort=row_labels, title=None),
    color=alt.Color("share:Q", scale=alt.Scale(domain=[0, 1], scheme="blues"),
                    title="share of row", legend=alt.Legend(format=".0%")),
).properties(width=600, height=180, title="Visit frequency x new items")
numbers = alt.Chart(grid).mark_text(fontSize=16).encode(
    x=alt.X("column:N", sort=col_order),
    y=alt.Y("row:N", sort=row_labels),
    text="count:Q",
    color=alt.condition(alt.datum.share > 0.5, alt.value("white"), alt.value("black")),
)
(boxes + numbers).save("figures/direction1_v1_frequency_grid.png", scale_factor=2)


# direction 2: every response on a real time axis
chart2 = alt.Chart(df).mark_point(filled=True, size=140, opacity=0.75).encode(
    x=alt.X("timestamp:T", title="when the response came in",
            scale=alt.Scale(domain=["2026-09-20", "2026-10-22"])),
    y=alt.Y("satisfaction:Q", title="overall satisfaction",
            scale=alt.Scale(domain=[0.5, 5.5]), axis=alt.Axis(values=[1, 2, 3, 4, 5])),
    shape=alt.Shape("location:N", title="location",
                    scale=alt.Scale(domain=["Lansing", "West Loop", "Unknown"],
                                    range=["circle", "diamond", "square"])),
    color=alt.Color("location:N", title="location",
                    scale=alt.Scale(domain=["Lansing", "West Loop", "Unknown"],
                                    range=["#4c78a8", "#e45756", "#888888"])),
    tooltip=["timestamp", "location", "satisfaction", "comment"],
).properties(width=620, height=240, title="Satisfaction of each response over time")
chart2.save("figures/direction2_v1_response_timeline.png", scale_factor=2)


# direction 3: one mark per person, grouped by age range
group_order = ["Pizza only", "Pizza + something else", "No pizza", "Unclear"]
d3 = df.copy()
d3["age_range"] = pd.Categorical(d3["age_range"], age_order, ordered=True)
d3["order_group"] = pd.Categorical(d3["order_group"], group_order, ordered=True)
d3 = d3.sort_values(["age_range", "order_group"])
d3["slot"] = d3.groupby("age_range", observed=True).cumcount() + 1
d3["age_label"] = d3["age_range"].astype(str) + " (n=" + d3.groupby("age_range", observed=True)["slot"].transform("max").astype(str) + ")"
age_labels = []
for a in age_order:
    age_labels.append(d3[d3["age_range"] == a]["age_label"].iloc[0])

chart3 = alt.Chart(d3).mark_point(filled=True, size=380).encode(
    x=alt.X("age_label:N", sort=age_labels, title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("slot:Q", title=None, axis=None),
    shape=alt.Shape("order_group:N", title="what they ordered", sort=group_order,
                    scale=alt.Scale(domain=group_order,
                                    range=["triangle-up", "square", "circle", "cross"])),
    color=alt.Color("order_group:N", title="what they ordered", sort=group_order,
                    scale=alt.Scale(domain=group_order,
                                    range=["#d95f02", "#1b9e77", "#7570b3", "#999999"])),
    tooltip=["age_range", "order_text"],
).properties(width=520, height=330, title="What each person ordered, by age range (1 mark = 1 person)")
chart3.save("figures/direction3_v1_age_order_units.png", scale_factor=2)

print("saved 3 charts")
