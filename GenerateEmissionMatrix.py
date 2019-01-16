# -*- coding: utf-8 -*-
import numpy as np
import re
import time
import pickle
#inputs = np.array([np.fromstring(line, sep=' ') for line in open('as_training.utf8', 'r').readlines()])
B_ct = 0 # begin of lexicon
E_ct = 0 # end of lexicon
M_ct = 0 # middle of lexicon
S_ct = 0 # a lexicon with only a letter
#transition matrix Aij=P(Cj|Ci)
#  B E M S
#B
#E
#M
#S
B=[]
E=[]
M=[]
S=[]
#emission matrix Bij=P(Oj|Ci)
# o1 o2 o3 .....
#B
#E
#M
#S
All_letters_dict = dict()
B_dict = dict()
E_dict = dict()
M_dict = dict()
S_dict = dict()
def getChinese(context):
    # context = context.replace("1","一")
    # context = context.replace("2","二")
    # context = context.replace("3","三")
    # context = context.replace("4","四")
    # context = context.replace("5","五")
    # context = context.replace("6","六")
    # context = context.replace("7","七")
    # context = context.replace("8","八")
    # context = context.replace("9","九")
    # context = context.replace("0","零")
    filtrate = re.compile(u'[^\u4E00-\u9FA5]') # non-Chinese unicode range
    ret = filtrate.sub(r'', context) # remove all non-Chinese characters
    return ret
def add_to_dict(letter,dict_name):
    if letter not in dict_name:
        dict_name[letter] = 1
    else:
        dict_name[letter] = dict_name[letter] + 1
ct = 0
#,'../gold/as_training_words.utf8'
training_list = ['../training/as_training.utf8']
for train in training_list:  
    print(train)   
    for line in open(train, 'r').readlines():
        #line = line.decode("utf-8")
        for p_word in line.split():
            word = getChinese(p_word)
            #print(word) 
            if(word==''):
                #doEnglish and punc
                S_ct = S_ct+1
                S.append(p_word)
                add_to_dict(p_word,S_dict)
                add_to_dict(p_word,All_letters_dict)
            else:
                if(len(word)==1):
                    S_ct = S_ct+1
                    S.append(word)
                    add_to_dict(word,S_dict)
                    #all_letters.append(word)
                    add_to_dict(word,All_letters_dict)
                else:
                    B_ct = B_ct + 1
                    M_ct = M_ct + len(word) - 2
                    E_ct = E_ct + 1
                    B.append(word[0])
                    #all_letters.append(word[0])
                    add_to_dict(word[0],All_letters_dict)
                    add_to_dict(word[0],B_dict)
                    E.append(word[-1])
                    #all_letters.append(word[-1])
                    add_to_dict(word[-1],All_letters_dict)
                    add_to_dict(word[-1],E_dict)
                    for i in range(len(word)-2):
                        M.append(word[i+1])
                        #all_letters.append(word[i+1])
                        add_to_dict(word[i+1],All_letters_dict)
                        add_to_dict(word[i+1],M_dict)
print("len of all words dictionary:",len(All_letters_dict))
emission = np.zeros((4,len(All_letters_dict)),dtype='double')
def state(index):
    if(index==0):
        return "B"
    if(index==1):
        return "E"
    if(index==2):
        return "M"
    if(index==3):
        return "S"
def insert_emission(dict_name,ct,index):
    
    dict_for_good_turing = dict()
    dict_for_good_turing[0] = 0
    Total_nm_in_observ = 0
    max_ct = 0;
    for item in All_letters_dict:
        if item in dict_name:
            Total_nm_in_observ = Total_nm_in_observ + dict_name[item]
            if(dict_name[item] > max_ct):
                max_ct = dict_name[item]
    for item in All_letters_dict:
        if item in dict_name:
            if dict_name[item] not in dict_for_good_turing: 
                dict_for_good_turing[dict_name[item]] = 1
            else:
                dict_for_good_turing[dict_name[item]] = dict_for_good_turing[dict_name[item]] + 1

        else:
            dict_for_good_turing[0] = dict_for_good_turing[0] + 1

    #good-turing
    # print("Total (seen event)*number in ",state(index)," is ",Total_nm_in_observ)
    #print("ct:",ct,"Total_nm_in_observ",Total_nm_in_observ)
    print("Total unseen event in ",state(index)," is ",dict_for_good_turing[0])  
    i = 0         
    for item in All_letters_dict:
        if(item in dict_name and dict_name[item] > 0 and dict_name[item] < max_ct):
            n_r_0  = dict_for_good_turing[dict_name[item]]
            k = 1
            while(dict_name[item] + k not in dict_for_good_turing):
                k = k + 1
                if(dict_name[item] + k > max_ct):
                    print("= =",dict_name[item] + k)

            n_r_1 = dict_for_good_turing[dict_name[item] + k]
            r_1 = dict_name[item] + k
            r_star = float(r_1) * float(n_r_1)/float(n_r_0)
            emission[index][i] = r_star/Total_nm_in_observ
        elif(item not in dict_name):
            #case r is 0 
            #dict_name[item] = 0
            n_r_0  = dict_for_good_turing[0]
            #k = 1 
            # while(0 + k not in dict_for_good_turing):
            #     k = k + 1
            # if(k>2):
            #     print("good turing is strange")
            n_r_1 = dict_for_good_turing[1]
            if dict_for_good_turing[1]==0:
                print("dict_for_good_turing[1]==0!")
                exit(1)
            r_star = float(n_r_1)/float(n_r_0)
            emission[index][i] = r_star/Total_nm_in_observ
        i = i + 1
insert_emission(B_dict,B_ct,0)
insert_emission(E_dict,E_ct,1)
insert_emission(M_dict,M_ct,2)
insert_emission(S_dict,S_ct,3)
with open('All_letters_dict.pickle', 'wb') as handle:
    pickle.dump(All_letters_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

file = open("EmissionMatrix.txt","w")
for i in range(4):
    for j in range(len(All_letters_dict)):
        file.write(str(emission[i][j])+" ")
    file.write("\n")
file = open("BEMSmap.txt","w")
file.write("B:")
for item in B:
        file.write("%s" % item.encode('utf8'))
file.write("\n")
file.write("E:")
for item in E:
        file.write("%s" % item.encode('utf8'))
file.write("\n")
file.write("M:")
for item in M:
        file.write("%s" % item.encode('utf8'))
file.write("\n")
file.write("S:")
for item in S:
        file.write("%s" % item.encode('utf8'))
file.write("\n")
np.save("EmissionMatrix",emission)
print("Generate EmissionMatrix.npy")



    
