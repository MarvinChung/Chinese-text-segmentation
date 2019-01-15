# -*- coding: utf-8 -*-
import numpy as np
import re
import time
from gensim.models.word2vec import Word2Vec
words = []
#inputs = np.array([np.fromstring(line, sep=' ') for line in open('as_training.utf8', 'r').readlines()])
transition = np.zeros((4,4),dtype='double')
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
#emission matrix Bij=P(Oj|Ci)
# o1 o2 o3 .....
#B
#E
#M
#S
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

pre_is = -1 #find the class of the end of the word


training_list = ['../training/as_training.utf8','../gold/as_training_words.utf8']
for train in training_list: 
    print(train)   
    for line in open(train, 'r').readlines():
        for p_word in line.split():
            #print(word)
            #time.sleep(1)
            word = getChinese(p_word)   
            if(word==''):
                flag = 1
                for i in p_word:
                    if(not i.isalpha()):
                        flag = 0
                        break
                if(flag==1):
                    #doEnglish
                    S_ct = S_ct+1
                    if(pre_is > -1):
                        transition[pre_is][3] = transition[pre_is][3] + 1    
                    pre_is = 3
                    words.append(word)
            else:
                words.append(word)    
                if(len(word)==1):
                    S_ct = S_ct+1
                    if(pre_is > -1):
                        transition[pre_is][3] = transition[pre_is][3] + 1    
                    pre_is = 3     
                else:
                    B_ct = B_ct + 1
                    M_ct = M_ct + len(word) - 2
                    E_ct = E_ct + 1
                    if(len(word) - 2 > 0):
                    	#B-M
                    	transition[0][2] = transition[0][2] + 1
                    	#M-E
                    	transition[2][1] = transition[2][1] + 1
                    	#M-M
                    	transition[2][2] = transition[2][2] + len(word) - 3
                    else:
                    	#B-E
                    	transition[0][1] = transition[0][1] + 1
                    if(pre_is > -1):
                    	transition[pre_is][0] = transition[pre_is][0] + 1 
                    pre_is = 1

model = Word2Vec(words)
P = np.array([B_ct,E_ct,M_ct,S_ct])
PI = np.zeros((4,1),dtype='double')
PI[0] = B_ct/(B_ct+S_ct)
PI[3] = S_ct/(B_ct+S_ct)

file = open("TransitionMatrix.txt", "w")
for i in range(4):
	for j in range(4):
		if(P[i]==0):
			continue
		transition[i][j] = transition[i][j]/P[i]
		file.write(str(transition[i][j])+" ")
	file.write("\n")
print(transition)
print(PI)
print(P)
np.save("TransitionMatrix",transition)
np.save("PI",PI)
np.save("NumsOfBEMS",P)
model.save('word2vec.model')
print("generate TransitionMatrix.npy")
print("generate PI.npy")
print("generate NumsOfBEMS.npy")
print("generate word2vec.model")
        




    
