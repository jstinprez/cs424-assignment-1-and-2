# Assignment 2

## Task 1: Revisit your data and questions
My dataset grew from 15 to 35 responses (Sept 21 to Oct 20). My corporate contact did send the printed box toppers, but they arrived after the Assignment 1 deadline, and 20 of the 35 responses came in after it. The data is still mostly from Lansing (30 responses). West Loop went from 1 response to 4, which is still too few to compare locations, and one person left the location blank. Satisfaction is almost all 5s (26 of 35), and the sample is self-selected, so it probably leans toward happy and engaged customers. I found a few problems with the data. The order question was free text, so I grouped orders by keyword, and I marked 3 answers ("nothing," "Delivery," and a blank) as unclear. One atmosphere rating was blank and I left it blank instead of guessing. I kept the original export unchanged and saved the cleaned version separately. My questions changed. I am keeping three: (1) does visit frequency relate to which new items people have tried or heard of, since only 7 of 35 have tried any; (2) do orders differ by age range, reworded because almost everyone orders pizza, so it is really about who orders more than pizza; and (3) how do satisfaction and response volume change over time, which is new because responses came in bursts. I dropped the location comparison because West Loop has only 4 responses, and the atmosphere question because it barely varies. My old question about the share who tried the new items is now part of question 1.


## Task 2: Prepare the data

The data goes through one script, `01_clean.py`. It reads the original Google Forms export (`data/survey-responses-a2.csv`) and writes the cleaned version to `data/survey_clean.csv`, which is what every chart uses. Running the script from the `assignment-2` folder rebuilds the processed file. No rows were dropped.

The main changes:
- Shortened the long question text into column names, and turned timestamps into dates and hours.
- Filled the blank location as "Unknown." The blank atmosphere rating stays blank.
- Put visit frequency and age range in their natural order so charts sort correctly.
- Split the new-items checkboxes into one true/false column per answer, then made a three-group summary: tried at least one, heard of them but haven't tried, and haven't heard of them. People who checked both "haven't tried" and "haven't heard" are in the last group.
- Sorted the typed-in orders into groups by keyword (pizza only, pizza plus something else, no pizza, unclear), because almost everyone orders pizza and the exact wording adds little.
- Flagged comments that mention price, since several do.

The keyword grouping is my own rule, so a few orders could be grouped wrong.

## Task 3: Explore the data
## Task 3: Explore the data

I made four quick charts to see what the data could support. Each one counts responses.

![Responses per day](figures/explore_1_responses_per_day.png)

Responses came in bursts, not steadily. Most arrived on Sept 26-27 (9 responses), Oct 9-10 (12), and Oct 13 (4), with none between Oct 14 and Oct 19. The bursts mostly follow when the box toppers were in stock at the stores, so this chart shows how my data was collected, not how customers behave. That matters for any time-based view, because a pattern over time here would mostly reflect the box toppers.

![Overall satisfaction](figures/explore_2_satisfaction_counts.png)

This one was not useful. 26 of 35 gave a 5, and nobody gave a 2. A chart of the distribution is basically one tall bar, so I will not use it as a main direction. The only real low rating is a 3 with a food rating of 1 (a comment about sauce and salt).

![Visit frequency by new items](figures/explore_3_frequency_by_new_items.png)

This was the most interesting chart. Only 7 of 35 have tried a new item. Among the 23 regulars, 9 have not heard of the new items at all. That is surprising since regulars see the menu the most. Regulars were 23 of the 35 responses, so the overall numbers mostly describe regulars, and the first-time row has only 4 people, so I can’t read much into it.

![Age range by order](figures/explore_4_age_by_order.png)

Almost everyone orders pizza. All 10 clear orders in the 55+ group are pizza only, while the 25-54 groups have a few people ordering salad, wings, or extras. The groups are different sizes, so counts can mislead, and any pattern here rests on very few people.

These charts changed my plan. The satisfaction chart showed there is too little variation to be a main chart, and the order chart showed I should compare "pizza only vs. more than pizza" instead of every order type.

## Task 4: Implement visualization alternatives
## Task 5: Interaction and multiple views
## Task 6: Iterate and refine
## Task 7: Current design
