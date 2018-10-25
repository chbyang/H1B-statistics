# visa-statistics

## Problem
A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application processing over the past years, trying to identify the occupations and states with the most number of approved H1B visas. She has found statistics available from the US Department of Labor and its Office of Foreign Labor Certification Performance Data. But while there are ready-made reports for 2018 and 2017, the site doesn’t have them for past years.

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.

Your code should be modular and reusable for future. If the newspaper gets data for the year 2019 (with the assumption that the necessary data to calculate the metrics are available) and puts it in the input directory, running the run.sh script should produce the results in the output folder without needing to change the code.
## Approach
Time Complexity: O(N)
1.Get a dict {key: occupation/state; val: freq}

for example: {software: 3; data: 5; accountants: 3 ; postdoc: 3;}

2.Reverse key and value. get a dict {key: freq; val: list(tilte/state)}

In this example: {3: [accountant, software, postdoc]; 5: [data]}

3.Scan reversed dic from largest possible freq to 1, add first 10 title/state(maybe smaller than 10)

In this example: 14 (3+3+3+5) is number of certified works, which is the largest possible freq. The first occupation is founded when scan to 5, then find accountant/software/postdoc when scan to 3. Here, only 4 kinds of occupations are found.

4. Need to sort title list before print in step 3 [accountant, software, postdoc], but the chance of having same count is really small, so time complexity is still O(N)

## Run
update 3 args to input/occupation_output/state_output

./run.sh
