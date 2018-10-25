'''
O(N) algorithm
1. Get a dict of title/state+ count.
for example: {software,3; data 5; accountants 3}
2. Reverse key and value. get a dict count+list(tilte/state)
{3,[accountant,software];5,[data]}
3. scan from 11 to 1 in last reversed dict, 11 is row name, which is the largest possible count
add firt 10 title/state.
In this example, data is first founded when scan to 5, then find accountant and software when scan to 3
Sort title list [accountant, software], but the chance of having same count is really small, 
so this algorithm is still O(N)
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

''' status can have differe column name but value always certified, so just search 'certified' in each line
08: APPROVAL_STATUS CERTIFIED
09: APPROVAL_STATUS CERTIFIED (efile)
09: STATUS CERTIFIED (icert)
10: STATUS CERTIFIED
11: STATUS CERTIFIED
12: STATUS CERTIFIED
13: STATUS CERTIFIED
14: STATUS CERTIFIED
15: CASE_STATUS CERTIFIED
16: CASE_STATUS CERTIFIED
17: CASE_STATUS CERTIFIED
'''

import sys
input=open(sys.argv[1] ,encoding="utf8")
output1=open(sys.argv[2],'w')
output2=open(sys.argv[3],'w')

K=10    #top K job titles or states

dict_occupation_freq={}     #occupation name and its freq 
dict_freq_occupation={}     #freq and a list of occupations having the same freq
dict_state_freq={}          #state name and its freq 
dict_freq_state={}          #freq and a list of states having the same freq

row=0                       
Occupation_idx=0            #index of occupation name column, it varies among documents
State_idx=0                 #index of state name column, it varies among document
#status_idx=0                #index of status

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
            '''
            if col_name=='APPROVAL_STATUS' or col_name=='STATUS' or col_name=='CASE_STATUS':        #possible status names
                status_idx=col 
            '''
            col+=1
    else:
        if 'CERTIFIED' not in linelist:
            row-=1
            continue
        name_occupation=linelist[Occupation_idx].strip('"')         #occupation name may have " in the beginning or end
        if name_occupation not in dict_occupation_freq:
            dict_occupation_freq[name_occupation]=1
        else:
            dict_occupation_freq[name_occupation]+=1
        if linelist[State_idx] not in dict_state_freq:
            dict_state_freq[linelist[State_idx]]=1
        else:
            dict_state_freq[linelist[State_idx]]+=1
    row+=1

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
