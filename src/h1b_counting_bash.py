'''
Time Complexity: O(N)

1.Get a dict {key: occupation/state; val: freq}

for example: {software: 3; data: 5; accountants: 3 ; postdoc: 3;}

2.Reverse key and value. get a dict {key: freq; val: list(occupation/state)}

In this example: {3: [accountant, software, postdoc]; 5: [data]}

3.Scan reversed dic from largest possible freq to 1, add first 10 occupation/state(maybe smaller than 10)

In this example: 14 (3+3+3+5) is number of certified works, which is the largest possible freq. 
The first occupation is founded when scan to 5, then find accountant/software/postdoc when scan to 3. 
Here, only 4 kinds of occupations are found.

4.Need to sort occupation list before print in step 3 [accountant, software, postdoc], 
but the chance of having same freq is really small, so time complexity is still O(N)
'''

'''
After read file structure documents, I find job title and work state columns can
have different names. Below are names of two columns from 08 to 17:
08: JOB_TITLE STATE_1
09: JOB_TITLE STATE_1 (efile)
09: LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE (icert)
10: LCA_CASE_SOC_NAME WORK_LOCATION_STATE1 (file structure: LCA_CASE_WORKLOC1_STATE)
11: LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE 
12: LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE
13: LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE
14: LCA_CASE_SOC_NAME LCA_CASE_WORKLOC1_STATE
15: SOC_NAME WORKSITE_STATE
16: SOC_NAME WORKSITE_STATE
17: SOC_NAME WORKSITE_STATE
'''

import sys
input=open(sys.argv[1] ,encoding="utf8")    #import data
output1=open(sys.argv[2],'w')               #output files
output2=open(sys.argv[3],'w')

K=10    #top K job titles or states

dict_occupation_freq={}     #occupation name and its freq 
dict_freq_occupation={}     #freq and a list of occupations having the same freq
dict_state_freq={}          #state name and its freq 
dict_freq_state={}          #freq and a list of states having the same freq

row=0                       
Occupation_idx=0            #index of occupation name column, it varies among documents
State_idx=0                 #index of state name column, it varies among document

# get dict_occupation_freq and dict_state_freq
for line in input:          #get one line
    linelist=line.split(';')    #split by ;
    if row == 0:                #the first line
        col=0
        for col_name in linelist:
            if col_name=='JOB_TITLE' or col_name=='LCA_CASE_SOC_NAME' or col_name=='SOC_NAME' :     #possible job title name
                if Occupation_idx==0 or col_name!='JOB_TITLE':      # if "JOB_TITLE" and other possible name both exists in the document, use other SOC name
                    Occupation_idx=col
            if col_name=='STATE_1' or col_name=='LCA_CASE_WORKLOC1_STATE' or col_name=='WORK_LOCATION_STATE1' or col_name=='WORKSITE_STATE': #candidates of state names
                State_idx=col
            col+=1
    else:
        if 'CERTIFIED' not in linelist:
            continue
        name_occupation=linelist[Occupation_idx].strip('"')         #occupation name may have " in the beginning or end, strip them
        if name_occupation not in dict_occupation_freq:
            dict_occupation_freq[name_occupation]=1
        else:
            dict_occupation_freq[name_occupation]+=1
        if linelist[State_idx] not in dict_state_freq:
            dict_state_freq[linelist[State_idx]]=1
        else:
            dict_state_freq[linelist[State_idx]]+=1
    row+=1      #calculate row. include column names,so data is row-1

#get dict_freq_occupation
for occupation,freq in dict_occupation_freq.items():
    if freq not in dict_freq_occupation:
        dict_freq_occupation[freq]=[occupation]
    else:
        dict_freq_occupation[freq].append(occupation)
#get dict_freq_state
for state,freq in dict_state_freq.items():
    if freq not in dict_freq_state:
        dict_freq_state[freq]=[state]
    else:
        dict_freq_state[freq].append(state)

res_occupation=[] 
res_state=[]

#output first 10 occupations
left=K
output1.write("TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
for count in range(row-1,0,-1):
    if left==0: break   #found 10,stop
    if count in dict_freq_occupation:
        dict_freq_occupation[count].sort(key=str.lower)     # if multiple occupations have the same freq, sort string
        for i in dict_freq_occupation[count]:
            if left>0:
                res_occupation.append(i)
                output1.write(i+";"+str(count)+";"+'{percent:.1%}'.format(percent=count/(row-1))+'\n')
                left-=1
            else:       #found 10,stop
                break
#output first 10 states   
left=K
output2.write("TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE\n")
for count in range(row-1,0,-1):
    if left==0: break
    if count in dict_freq_state:
        dict_freq_state[count].sort(key=str.lower)           # if multiple occupations have the same freq, sort string
        for i in dict_freq_state[count]:
            if left>0:
                res_state.append(i)
                output2.write(i+";"+str(count)+";"+'{percent:.1%}'.format(percent=count/(row-1))+'\n')
                left-=1
            else:
                break
            
#print(res_occupation, res_state)

input.close()
output1.close()
output2.close()
