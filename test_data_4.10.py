# -*- coding: utf-8 -*-
import json
import os,sys
import OptModul as opt
import numpy

Base_Path=sys.path[0]
filepath=os.path.join(Base_Path,"res.txt")
S_LinesDict=opt.GenSLinesDict_1(filepath)
filepath=os.path.join(Base_Path,"debug.B.txt")
T_LinesDict=opt.GenTLinesDict_1(filepath)
Ensemble=opt.GenStaticData(S_LinesDict,T_LinesDict)
StaticDict=Ensemble[0]
LocationData=Ensemble[1]
sum_word=opt.SumOfWord(StaticDict)
print(sum_word)
mean_result=opt.FindMeanVar(StaticDict)
InitClassifyDict=opt.InitClassify(mean_result,StaticDict)
right=259.02
left=232.85
OptThreshold=[]
OptThreshold.append(left)
OptThreshold.append(right)
StaticDate=opt.JudeThre(OptThreshold,StaticDict)
FindCla=opt.ResultOfCla(sum_word,OptThreshold,StaticDate)
print(OptThreshold)
print(FindCla)


filepath=os.path.join(Base_Path,"full_data_wrong.txt")
if ~os.path.exists(filepath):
    wrong_time=[]
    wrong_score=[]
    wrong_volume=[]
    fout=open(filepath,"w")
    for key in StaticDate:
        line_content=StaticDate[key]
        num_word=len(line_content)
        for index in range(num_word):
            word_content=line_content[index]
            if word_content[5]!=word_content[6]:
                wrong_time.append(word_content[1])
                wrong_score.append(word_content[3])
                wrong_volume.append(word_content[2])
                fout.write(str(word_content))
                fout.write("\n")
    w_time_m=numpy.mean(wrong_time)
    w_time_v=numpy.var(wrong_time)
    w_score_m=numpy.mean(wrong_score)
    w_score_v=numpy.var(wrong_score)
    w_volume_m=numpy.mean(wrong_volume)
    w_volume_v=numpy.var(wrong_volume)
    fout.close()

filepath=os.path.join(Base_Path,"full_data_true.txt")
if ~os.path.exists(filepath):
    right_time=[]
    right_score=[]
    right_volume=[]
    fout=open(filepath,"w")
    for key in StaticDate:
        line_content=StaticDate[key]
        num_word=len(line_content)
        for index in range(num_word):
            word_content=line_content[index]
            if word_content[5]==word_content[6]:
                right_time.append(word_content[1])
                right_score.append(word_content[3])
                right_volume.append(word_content[2])
                fout.write(str(word_content))
                fout.write("\n")
    r_time_m=numpy.mean(right_time)
    r_time_v=numpy.var(right_time)
    r_score_m=numpy.mean(right_score)
    r_score_v=numpy.var(right_score)
    r_volume_m=numpy.mean(right_volume)
    r_volume_v=numpy.var(right_volume)
    fout.close()


print(w_time_m,'  ',w_time_v)
print(r_time_m,'  ',r_time_v)
print(w_score_m,'  ',w_score_v)
print(r_score_m,'  ',r_score_v)
print(w_volume_m,'  ',w_volume_v)
print(r_volume_m,'  ',r_volume_v)



