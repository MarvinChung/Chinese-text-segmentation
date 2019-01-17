**Chinese-Text-Segmentaion Using HMM**


---
**references:**
1.fukuball 文章:
> https://speakerdeck.com/fukuball/head-first-chinese-text-segmentation?slide=45

2.Itenyh版-用HMM做中文分词四：A Pure-HMM 分词器
> http://www.52nlp.cn/itenyh%E7%89%88-%E7%94%A8hmm%E5%81%9A%E4%B8%AD%E6%96%87%E5%88%86%E8%AF%8D%E5%9B%9B%EF%BC%9Aa-pure-hmm-%E5%88%86%E8%AF%8D%E5%99%A8

**Sources**
1.SIGHAN提供2005年非商業用途的corpus source : 
> http://sighan.cs.uchicago.edu/bakeoff2005/

2.音樂歌詞source:
> 霆哥的2.3萬首歌詞(2004年前)
https://onedrive.live.com/embedrow.aspx/%E5%85%AC%E9%96%8B/%E9%9C%86%E5%93%A5blog/lrcc.rar?cid=afead2c662efe856
作者部落格：http://tinggotw.pixnet.net/blog/post/36850501#comment-form

**python3 is needed!**

Generate TransitionMatrix.npy, PI.npy, NumsOfBEMS.npy
```
python3 GenerateTransitionMatrix.py
```
Generate EmissionMatrix.npy, All_letters_dict.pickle
```
python3 GenerateEmissionMatrix.py
```
Check the states are sum to 1
```
python3 CheckEmissionMatrix.py
```
Chinese-segmentation 
```
python3 Viterbi $i $j
(i=0: show state details)
(i=1: no details ,default)
(j=0: split with "/")
(j=1: split with " ", default)
```

Generate idf_dict.pickle
```
python3 GenerateIDF.py
```

Find the most significant words in the songs
```
python3 ExtractFeature.py
```