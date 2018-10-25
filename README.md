# visa-statistics

## Problem

## Approach
Time Complexity: O(N)
1. Get a dict {key: occupation/state, val: freq}
for example: {software: 3; data: 5; accountants: 3 ; postdoc: 3;}
2. Reverse key and value. get a dict {key: freq, val: list(tilte/state)}
{3,[accountant,software,postdoc];5,[data]}
3. Scan from 11 to 1 in last reversed dict, 11 is number of certified, which is the largest possible freq, add fisrt 10 title/state.
In this example, first occupation is founded when scan to 5, then find accountant/software/postdoc when scan to 3
Sort title list [accountant, software, postdoc], but the chance of having same count is really small, so time complexity is still O(N)

## Run
update 3 args to input/occupation_output/state_output
./run.sh
