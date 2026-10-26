import altair as alt
import pandas as pd

df = pd.read_csv("data/processed/survey_clean.csv")
df["comment"] = df["comment"].fillna("")
df["order_text"] = df["order_text"].fillna("")

freq_order = ["First Time", "Occasionally", "Regularly"]
status_order = ["Tried at least one", "Heard of them, haven't tried", "Haven't heard of them"]

# row labels like "Regularly (n=23)"
sizes = df.groupby("visit_freq").size()
df["row"] = df["visit_freq"].map(lambda f: f + " (n=" + str(sizes[f]) + ")")
row_labels = [f + " (n=" + str(sizes[f]) + ")" for f in freq_order]

# data for the bars
rows = []
for freq in freq_order:
    label = freq + " (n=" + str(sizes[freq]) + ")"
    group = df[df["visit_freq"] == freq]
    start = 0
    for status in status_order:
        count = int((group["new_items_status"] == status).sum())
        share = count / len(group)
        rows.append({"row": label, "status": status, "count": count,
                     "percent": str(round(share * 100)) + "%",
                     "start": start, "end": start + share, "middle": start + share / 2})
        start = start + share
bars_df = pd.DataFrame(rows)

# data for the list of people
people = pd.DataFrame({
    "row": df["row"],
    "status": df["new_items_status"],
    "info": df["age_range"] + "  |  " + df["order_text"].str.slice(0, 26),
    "comment": df["comment"],
    "comment_short": df["comment"].map(lambda c: c[:62] + "..." if len(c) > 62 else (c if c else "(no comment)")),
    "order_text": df["order_text"],
})


def make_chart(start_selection=None):
    # start_selection is only used to make the screenshot with a bar already clicked
    if start_selection:
        pick = alt.selection_point(fields=["row", "status"], empty=False, value=[start_selection])
    else:
        pick = alt.selection_point(fields=["row", "status"], empty=False)

    colors = alt.Scale(domain=status_order, range=["#08519c", "#6baed6", "#fdae6b"])

    bars = alt.Chart(bars_df).mark_bar().encode(
        x=alt.X("start:Q", title="share of people in that group", axis=alt.Axis(format="%")),
        x2="end:Q",
        y=alt.Y("row:N", sort=row_labels, title=None),
        color=alt.Color("status:N", scale=colors, sort=status_order, title="new items"),
        stroke=alt.condition(pick, alt.value("black"), alt.value("white")),
        strokeWidth=alt.condition(pick, alt.value(3), alt.value(1)),
        tooltip=["row", "status", "count", "percent"],
    ).add_params(pick).properties(width=380, height=200, title="Have visitors tried the new items?")

    numbers = alt.Chart(bars_df[bars_df["count"] > 0]).mark_text(fontSize=15).encode(
        x="middle:Q",
        y=alt.Y("row:N", sort=row_labels),
        text="count:Q",
        color=alt.condition(alt.datum.status == "Tried at least one", alt.value("white"), alt.value("black")),
    )

    base = alt.Chart(people).transform_filter(pick).transform_window(rank="row_number()")
    y_pos = alt.Y("rank:Q", axis=None, scale=alt.Scale(domain=[10, 0]))
    info = base.mark_text(align="left", x=0, fontSize=12).encode(
        y=y_pos, text="info:N", tooltip=["row", "status", "order_text", "comment"])
    comment = base.mark_text(align="left", x=220, fontSize=12, color="#444444").encode(
        y=y_pos, text="comment_short:N", tooltip=["comment"])
    who = (info + comment).properties(
        width=560, height=260,
        title={"text": "Who is in the clicked bar?",
               "subtitle": "age  |  what they ordered          what they said (click a bar to fill this in)"})

    return alt.hconcat((bars + numbers), who).resolve_scale(color="independent")


# the interactive page
make_chart().save("figures/task5_interactive.html", inline=True)

# screenshots for the report
make_chart().save("figures/task5_interactive_start.png", scale_factor=2)
make_chart({"row": "Regularly (n=23)", "status": "Haven't heard of them"}).save(
    "figures/task5_interactive_clicked.png", scale_factor=2)

print("saved visualization.html and two screenshots")
