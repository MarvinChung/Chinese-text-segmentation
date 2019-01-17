import os
import io
import re
import sys
import subprocess
import pickle
import math
import threading
from subprocess import run, PIPE
inv_idf_dict = {}
idf_dict = {}
file_ct = 0
max_thread = 70
"""
Viterbi_path = "Viterbi.py"
def child(r, w):
    read_file = os.fdopen(r, 'r')
    write_file = os.fdopen(w, 'w')
    os.dup2(r,0)
    os.dup2(w,1)
    os.execl("/Library/Frameworks/Python.framework/Versions/3.6/bin/python3","/Library/Frameworks/Python.framework/Versions/3.6/bin/python3",Viterbi_path)    

      
def split_process(path):
    r, w = os.pipe()
    if os.fork() == 0:
        child(r, w)
    else:
        w_file = os.fdopen(w, 'w')
        r_file = os.fdopen(r, 'r')
        read_all_lyrics(r_file,w_file,path)
 """       

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
def read_lyric(dirPath,fileNames):
    for f in fileNames:
        if(f.find(".lrc")>0):
            print(dirPath+"/"+f)
            f = open(dirPath+"/"+f , "rb")
            text = f.read().decode('big5',errors='ignore').encode('utf-8').decode('utf-8')
            str = ""
            for line in text.splitlines():
                #print(line)
                line = line.replace("[ti:LRC之家歌詞大賞]","")
                line = line.replace("[ar:LRC之家歌詞大賞]","")
                line = line.replace("[al:LRC之家歌詞大賞]","")
                line = line.replace("[by:LRC之家 http://www.abclrc.com]","")
                str = str + getChinese(line) + "\n"
            
            p = run(["python3","Viterbi.py"], stdout=PIPE, input=str, encoding='utf-8')
            #print(p.stdout)
            words = p.stdout.split()
            temp_dict = {}
            f.close()
            with lock:
                global file_ct
                file_ct += 1
                for word in words:
                    if word not in temp_dict:
                        temp_dict[word] = 1
                        if word not in inv_idf_dict:
                            inv_idf_dict[word] = 1
                        else:
                            inv_idf_dict[word] = inv_idf_dict[word] + 1
def split_list(arr, size):
     arrs = []
     
     need_thread = 1
     while len(arr) > size and need_thread < max_thread:
         pice = arr[:size]
         arrs.append(pice)
         arr   = arr[size:]
         need_thread = need_thread + 1
     arrs.append(arr)
     return arrs,need_thread

if __name__ == '__main__':
    path = "./lrcc"
    for dirPath, dirNames, fileNames in os.walk(path):
        threads = []
        print(len(fileNames))
        avg = 1
        if(max_thread > len(fileNames)):
            avg = 1
        else:
            avg = int(len(fileNames)/max_thread)
        arrs,thread_n = split_list(fileNames,avg)
        print("given thread n:",thread_n)
        for i in range(thread_n ):
            global lock
            lock = threading.Lock()
            threads.append(threading.Thread(target = read_lyric , args = (dirPath,arrs[i],)))
            threads[i].start()
        for i in range(thread_n ):
            threads[i].join()
        #print dirPath
        #p=subprocess.Popen(["python3","Viterbi.py"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)

        
    for key in inv_idf_dict:
        idf_dict[key] = math.log10(file_ct/(1+inv_idf_dict[key]))
    with open('idf_dict.pickle', 'wb') as handle:
        pickle.dump(idf_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    #split_process(path)