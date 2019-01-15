#encoding=utf-8
#print("wait for python ready...")
import pickle
import math
import numpy as np
import re
import sys
from gensim.models.word2vec import Word2Vec
#w2v_model = Word2Vec.load('word2vec.model')
with open('All_letters_dict.pickle', 'rb') as handle:
    All_letters_dict = pickle.load(handle)
#for item in All_letters_dict:
#   print(item)
#print(len(All_letters_dict))
emission = np.load("EmissionMatrix.npy")
transition = np.load("TransitionMatrix.npy")
NumsOfBEMS = np.load("NumsOfBEMS.npy")
PI = np.load("PI.npy")
All_cts = np.sum(NumsOfBEMS)
B_prob = NumsOfBEMS[0]/All_cts
E_prob = NumsOfBEMS[1]/All_cts
M_prob = NumsOfBEMS[2]/All_cts
S_prob = NumsOfBEMS[3]/All_cts
emission = emission
def StateToBEMS(state):
    if state == 0:
        return "B"
    elif state == 1:
        return "E"
    elif state == 2:
        return "M"
    elif state == 3:
        return "S"
def getProb(state,observ):
    #OOV case
    if observ not in All_letters_dict:
        #substitute =  w2v_model.wv.most_similar(observ, topn=1)
        #return getProb(state,substitute)
        if state == 0:
            return B_prob
        elif state == 1:
            return E_prob
        elif state == 2:
            return M_prob
        elif state == 3:
            return S_prob
    else:
        return emission[state][list(All_letters_dict.keys()).index(observ)]
def Viterbi(observSeq,mode,seg):
    #observSeq = observSeq.decode("utf-8")
    chinese_word = []
    english_character = ""
    words = []
    non_punc = []
    #print(observSeq)
    backpath = []
    for character in observSeq:
        if character >= u'\u4E00' and character <= u'\u9FA5':
            if(len(english_character)>0):
                words.append(english_character)
                non_punc.append(english_character)
                english_character = ""
            chinese_word.append(character)
            non_punc.append(character)
            words.append(character)
        elif(character.isalpha()):
            english_character = english_character + character
        else:
            if(len(english_character)>0):
                words.append(english_character)
                non_punc.append(english_character)
                english_character= ""
            if(character!=" "):
                words.append(character)
    if(len(english_character)>0):
        words.append(english_character)
        non_punc.append(english_character)
        english_character = ""
    #print(words)
    if(len(non_punc)>0):
        delta = np.zeros((4,len(All_letters_dict)),dtype='double')
        pre = np.zeros((4,len(All_letters_dict)),dtype='int')
        #initialize
        for i in range(4):
            delta[i][0] = PI[i][0] * getProb(i,non_punc[0])
        #start viterbi
        for i in range(1,len(chinese_word),1):
            for j in range(4):
                delta[j][i] = getProb(j,non_punc[i]) * np.max([delta[state][i-1]*transition[state][j] for state in range(4)])
                pre[j][i] = np.argmax([delta[state][i-1]*transition[state][j] for state in range(4)])
                #print(i,j,"is",delta[j][i])
                #print("transition",transition)
                #print("pre is",pre[j][i],"p:",np.max([delta[state][i-1]*transition[state][j] for state in range(4)]))
                #for state in range(4):
                #   print("p:","state:",state,"j",j,delta[state][i-1]*transition[state][j])

        
        #print("wtf",np.max([delta[state][len(chinese_word)-1] for state in range(4)]))
        #print("wtf2",np.argmax([delta[state][len(chinese_word)-1] for state in range(4)]))
        next_pre = np.argmax([delta[state][len(non_punc)-1] for state in range(4)])
        #print("next_pre",next_pre)
        backpath.append(StateToBEMS(next_pre))
        backpath.append(non_punc[-1])
        for i in range(len(non_punc)-2,-1,-1):
            next_pre = pre[next_pre][i+1]
            #print("next_pre",next_pre)
            backpath.append(StateToBEMS(next_pre))
            backpath.append(non_punc[i]) 
        backpath.reverse()
        if(int(mode) == 0):
            print(backpath)
    ct = 0
    output = ""
    pre = ""
    if(int(seg) == 0):
        seg_word = "/"
    if(int(seg) == 1):
        seg_word = " "

    for i in range(len(words)):
        if(len(backpath)>0 and ct < len(backpath) and words[i]==backpath[ct]):       
            if(backpath[ct+1]=="E" or backpath[ct+1]=="S"):
                output=output+words[i]+seg_word
            elif(backpath[ct+1]=="B" and (pre!="E" and pre!="S" and pre!="")):
                output=output+seg_word+words[i]
            else:
                output=output+words[i]
            pre = backpath[ct+1]
            ct = ct + 2
        else:
            output=output+words[i]+seg_word
    #print(words)
    #print(non_punc)
    print(output)
if __name__ == '__main__':
    mode = 1
    seg = 1
    #print("用法:python3 Viterbi $(0 output details, 1 output results with only results) $(輸入間隔要用什麼符號, 0用/,1用空白間格) ")
    #print("no argvs , default python3 Viterbi 1 1")
    if(len(sys.argv)>1):
        mode = sys.argv[1]
    if(len(sys.argv)>2):
        seg = sys.argv[2]
    #print(mode)
    #while(observSeq=input("")):
    #    Viterbi(observSeq,mode,seg)
    for line in sys.stdin:
        if(line[len(line)-1]=="\n"):
            line = line[:-1]
        Viterbi(line,mode,seg)
