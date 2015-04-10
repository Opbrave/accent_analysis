# -*- coding: utf-8 -*-
import json
import os,sys
import pylab
import math
import numpy

def GenSLinesDict(FileIn): #the data is: 276./tone_liye	Excuse:1 me:2
    '''
    读取人工标注文本，
    获得单词与类别的匹配Dict
    '''
    fin=open(FileIn,"r")
    S_LinesDict={}
    for line in fin:
        wordlist=line.strip().split(".")
        if len(wordlist) !=2:
            print("The struct of data is wrong")
        tmpstr_1="".join(wordlist[1:])
        wordlist_1=tmpstr_1.strip().split()
        num_wordlist_1=len(wordlist_1)
        linelist=[]  #修改
        for word_index in range(num_wordlist_1-1):
            tmpword=str(wordlist_1[word_index+1]).split(":")
            if len(tmpword)==2:
                tmplist=[]
                tmplist.append(tmpword[0])
                tmplist.append(int(tmpword[1]))
                linelist.append(tmplist)
        S_LinesDict[str(wordlist[0]).strip()]=linelist
    fin.close()
    return S_LinesDict

def GenSLinesDict_1(FileIn): #the data is: 165941_2.wav	"Are^2|you^2|okay^1|sil^0|"
    fin=open(FileIn,"r")
    textdict={}
    for line in fin:
        wordlist=line.strip().split()
        tmp_str=wordlist[0].strip().split(".")
        keyname=tmp_str[0]
        sent=wordlist[1].strip('"')
        wordlist_1=sent.strip('|').split('|')
        wordnum=len(wordlist_1)
        linelist=[]
        for index in range(wordnum):
            wordlist=[]
            wordlist_2=wordlist_1[index].strip().split('^')
            if wordlist_2[0]=='sil':
                continue
            try:
                int(wordlist_2[1])
            except:
                continue
            if int(wordlist_2[1])>10:
                data_int=int(wordlist_2[1])
                data_sum=data_int/10+data_int%10
                if data_sum==3:
                    wordlist_2[1]=2
                elif data_sum==4:
                    wordlist_2[1]=2
                elif data_sum==5:
                    wordlist_2[1]=3
            wordlist.append(wordlist_2[0])
            wordlist.append(int(wordlist_2[1]))
            linelist.append(wordlist)
        if keyname not in textdict:
            #print(keyname)
            textdict[keyname]=linelist
    fin.close()
    return textdict
    
def GenTLinesDict(FileIn): #no time, score, volume
    '''
    读取机器标注的文本
    获取文本内容，以及音调评分值
    '''
    fin=open(FileIn,'r')
    T_LinesDict={}
    for line in fin:
        m_wordlist=line.split()
        m_str=m_wordlist[0].strip()
        m_wordlist_1=m_str.split(".")
        m_str_1=m_wordlist_1[0]
        m_wordlist_2=m_str_1.split("/")
        m_name=m_wordlist_2[-1]
        num_lines=0
        wordlist=line.split()
        strdata="".join(wordlist[1:])
        aa=json.loads(strdata)
        _line_content = aa["lines"]
        num_line_content = len(_line_content)
        LineList=[] #
        num_LineDict=0
        for index_line_ in range(0,num_line_content):
            line_result = _line_content[index_line_]
            if line_result.has_key("sample"):
                line_sample=line_result["sample"]
                #print(line_sample)
            if line_result.has_key("words"):
                words_result=line_result["words"]
                num_words_result=len(words_result)
                for words_index in range(num_words_result):
                    word_content=words_result[words_index]
                    word_type=word_content["type"]
                    if word_type !=2:
                        continue     
                    tmplist=[]
                    tmplist.append(word_content["text"])
                    tmplist.append(word_content["accent"])
                    LineList.append(tmplist)
                    num_LineDict+=1
        T_LinesDict[m_name]=LineList
        #print(m_name)
    return T_LinesDict

def GenTLinesDict_1(FileIn):
    fin=open(FileIn,'r')
    T_LinesDict={}
    for line in fin:
        m_wordlist=line.split()
        m_str=m_wordlist[0].strip()
        m_wordlist_1=m_str.split(".")
        m_str_1=m_wordlist_1[0]
        m_wordlist_2=m_str_1.split("/")
        m_name=m_wordlist_2[-1]
        num_lines=0
        wordlist=line.split()
        strdata="".join(wordlist[1:])
        aa=json.loads(strdata)
        _line_content = aa["lines"]
        num_line_content = len(_line_content)
        LineList=[] #
        num_LineDict=0
        for index_line_ in range(0,num_line_content):
            line_result = _line_content[index_line_]
            if line_result.has_key("sample"):
                line_sample=line_result["sample"]
            if line_result.has_key("words"):
                words_result=line_result["words"]
                num_words_result=len(words_result)
                for words_index in range(num_words_result):
                    word_content=words_result[words_index]
                    word_type=word_content["type"]
                    word_begin=word_content["begin"]
                    word_end=word_content["end"]
                    time_last=float(word_end)-float(word_begin)
                    word_volume=word_content["volume"]
                    word_score=word_content["score"]
                    if word_type !=2:
                        continue
                    tmplist=[]
                    tmplist.append(word_content["text"])
                    tmplist.append(time_last)
                    tmplist.append(word_volume)
                    tmplist.append(word_score)
                    tmplist.append(word_content["accent"])
                    LineList.append(tmplist)
                    num_LineDict+=1
        T_LinesDict[m_name]=LineList
    return T_LinesDict
                      
def GenStaticData(S_LinesDict,T_LinesDict):
    '''
    获得机器标注对象中单词对应人工标注的类别，及声调值
    '''
    num_T=len(T_LinesDict)
    Static_Data={}#get the float data of every label
    for key_0 in S_LinesDict:
        if key_0 in T_LinesDict:
            m_list_S=S_LinesDict[key_0]
            m_list_T=T_LinesDict[key_0]
            num_S_list=len(m_list_S)
            num_T_list=len(m_list_T)
            index_T=0
            index_S=0
            index_list=0
            list_tmp=[]
            same_count=0
            error_S=0
            error_T=0
            while index_T<num_T_list-1 and index_S<num_S_list-1:
                if str(m_list_S[index_S][0])==str(m_list_T[index_T][0]):
                    m_list_T[index_T].append(m_list_S[index_S][1])
                    list_tmp.append(m_list_T[index_T])
                    index_T+=1
                    index_S+=1
                    same_index_S=index_S
                else:
                    index_S+=1
                    error_S+=1
                if error_S>=2:  #not stable!!!
                    index_S=index_S-error_S
                    index_T+=1
                    error_S=0
            Static_Data[key_0]=list_tmp
            list_tmp=[]
    lablist_1=[]
    lablist_2=[]
    lablist_3=[]
    for key in Static_Data:
        linecon=Static_Data[key]
        for index in range(len(linecon)):
            if linecon[index][5]==1:
                lablist_1.append(linecon[index])
            elif linecon[index][5]==2:
                lablist_2.append(linecon[index])
            else:
                lablist_3.append(linecon[index])
    StaticData={}
    StaticData["1"]=lablist_1
    StaticData["2"]=lablist_2
    StaticData["3"]=lablist_3
    Ensemble=[]
    Ensemble.append(StaticData)
    Ensemble.append(Static_Data)
    return Ensemble

def SumOfWord(StaticDict):
    wordsum=0
    for key in StaticDict:
        linecon=StaticDict[key]
        for index in range(len(linecon)):
            wordsum+=1
    return wordsum

def FindMeanVar(StaticDict):
    label1_float=[]
    label2_float=[]
    label3_float=[]
    result=[]
    labdata_1=StaticDict["1"]
    labdata_2=StaticDict["2"]
    labdata_3=StaticDict["3"]
    for n in range(len(labdata_1)):
        label1_float.append(labdata_1[n][4])
    for n in range(len(labdata_2)):
        label2_float.append(labdata_2[n][4])
    for n in range(len(labdata_1)):
        label3_float.append(labdata_3[n][4])
    mean_1=numpy.mean(label1_float)
    var_1=numpy.var(label1_float)
    mean_2=numpy.mean(label2_float)
    var_2=numpy.var(label2_float)
    mean_3=numpy.mean(label3_float)
    var_3=numpy.var(label3_float)
    result.append(mean_1)
    result.append(var_1)
    result.append(mean_2)
    result.append(var_2)
    result.append(mean_3)
    result.append(var_3)
    return result

def GenPlot(StaticDict):
    label1_float=[]
    label2_float=[]
    label3_float=[]
    result=[]
    labdata_1=StaticDict["1"]
    labdata_2=StaticDict["2"]
    labdata_3=StaticDict["3"]
    for n in range(len(labdata_1)):
        label1_float.append(labdata_1[n][4])
    for n in range(len(labdata_2)):
        label2_float.append(labdata_2[n][4])
    for n in range(len(labdata_1)):
        label3_float.append(labdata_3[n][4])
    pylab.plot(range(len(label1_float)),label1_float,'ro',range(len(label2_float)),\
               label2_float,'bo',range(len(label3_float)),label3_float,'go')
    pylab.show()
    return 1
    
def InitClassify(result,StaticDict):
    right=result[1]
    left=result[4]
    thre_right=right
    thre_left=left
    for key in StaticDict:
        line_content=StaticDict[key]
        num_line_content=len(line_content)
        for index in range(num_line_content):
            if line_content[index][4]<thre_left:
                line_content[index].append(3)
            elif line_content[index][4]>thre_right:
                line_content[index].append(1)
            else:
                line_content[index].append(2)
    return StaticDict


def JudeThre(thre,StaticDate):
    left=thre[0]
    right=thre[1]
    for key in StaticDate:
        linecontent=StaticDate[key]
        for index in range(len(linecontent)):
            if linecontent[index][4]<left:
                linecontent[index][6]=3
            elif linecontent[index][4]>right:
                linecontent[index][6]=1
            else:
                linecontent[index][6]=2
    return StaticDate

def ResultOfCla(wordsum,thre,StaticDict): #the result of classification
    right=thre[1]
    left=thre[0]
    thre_right=right
    thre_left=left
    err_1=0
    err_2=0
    err_3=0
    cornum=0.0
    rate=0.0
    labeldata_1=StaticDict["1"]
    labeldata_2=StaticDict["2"]
    labeldata_3=StaticDict["3"]
    for n in range(len(labeldata_1)):
        if labeldata_1[n][5]==labeldata_1[n][6]:
            cornum+=1
        else:
            err_1+=1
    for n in range(len(labeldata_2)):
        if labeldata_2[n][5]==labeldata_2[n][6]:
            cornum+=1
        else:
            err_2+=1
    for n in range(len(labeldata_3)):
        if labeldata_3[n][5]==labeldata_3[n][6]:
            cornum+=1
        else:
            err_3+=1
    rate=cornum/wordsum
    cla_result={}
    cla_result["1"]=err_1
    cla_result["2"]=err_2
    cla_result["3"]=err_3
    cla_result["rate"]=rate
    return cla_result
    
    
def Location(OptThreshold,StaticLocation):
    left=OptThreshold[0]
    right=OptThreshold[1]
    for key in StaticLocation:
        m_list=StaticLocation[key]
        for index in range(len(m_list)):
            if m_list[index][4]<left:
                m_list[index][6]=3
            elif m_list[index][4]>right:
                m_list[index][6]=1
            else:
                m_list[index][6]=2
    return StaticLocation

def WrongRate(Sumword,OptThreshold,StaticLocation):
    left=OptThreshold[0]
    right=OptThreshold[1]
    wrongnum=0.0
    rate=0.0
    for key in StaticLocation:
        m_list=StaticLocation[key]
        for index in range(len(m_list)):
            if abs(m_list[index][5]-m_list[index][6])==2:
                wrongnum+=1
    rate=wrongnum/Sumword
    return rate
###
