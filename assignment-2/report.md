# Assignment 2

## Task 1: Revisit your data and questions
My dataset grew from 15 to 35 responses (Sept 21 to Oct 20). My corporate contact did send the printed box toppers, but they arrived after the Assignment 1 deadline, and 20 of the 35 responses came in after it. The data is still mostly from Lansing (30 responses). West Loop went from 1 response to 4, which is still too few to compare locations, and one person left the location blank. Satisfaction is almost all 5s (26 of 35), and the sample is self-selected, so it probably leans toward happy and engaged customers. I found a few problems with the data. The order question was free text, so I grouped orders by keyword, and I marked 3 answers ("nothing," "Delivery," and a blank) as unclear. One atmosphere rating was blank and I left it blank instead of guessing. I kept the original export unchanged and saved the cleaned version separately. My questions changed. I am keeping three: (1) does visit frequency relate to which new items people have tried or heard of, since only 7 of 35 have tried any; (2) do orders differ by age range, reworded because almost everyone orders pizza, so it is really about who orders more than pizza; and (3) how do satisfaction and response volume change over time, which is new because responses came in bursts. I dropped the location comparison because West Loop has only 4 responses, and the atmosphere question because it barely varies. My old question about the share who tried the new items is now part of question 1.


## Task 2: Prepare the data

The data goes through one script, `code/01_clean.py`. It reads the original Google Forms export (`data/original/survey-responses-a2.csv`) and writes the cleaned version to `data/processed/survey_clean.csv`, which is what every chart uses. Running the script from the `assignment-2` folder rebuilds the processed file. No rows were dropped.

The main changes:
- Shortened the long question text into column names, and turned timestamps into dates and hours.
- Filled the blank location as "Unknown." The blank atmosphere rating stays blank.
- Put visit frequency and age range in their natural order so charts sort correctly.
- Split the new-items checkboxes into one true/false column per answer, then made a three-group summary: tried at least one, heard of them but haven't tried, and haven't heard of them. People who checked both "haven't tried" and "haven't heard" are in the last group.
- Sorted the typed-in orders into groups by keyword (pizza only, pizza plus something else, no pizza, unclear), because almost everyone orders pizza and the exact wording adds little.
- Flagged comments that mention price, since several do.

The keyword grouping is my own rule, so a few orders could be grouped wrong.

## Task 3: Explore the data
## Task 4: Implement visualization alternatives
## Task 5: Interaction and multiple views
## Task 6: Iterate and refine
## Task 7: Current design
