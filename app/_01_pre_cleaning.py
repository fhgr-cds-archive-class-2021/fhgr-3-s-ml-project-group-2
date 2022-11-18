import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


#Read data from file
data = pd.read_csv("../beijing.csv", encoding="iso-8859-1", delimiter=",")
gbkdata = pd.read_csv("../beijing.csv", encoding="gbk", delimiter=",")


#drop usless columns
df = data.drop(['url', 'id', 'Cid', 'DOM', 'price', 'followers'], axis=1)


#Datetime split
df["tradeTime"]=pd.to_datetime(df["tradeTime"])
df['tradeYear']=df['tradeTime'].dt.year
df['tradeMonth']=df['tradeTime'].dt.month
df['tradeDay']=df['tradeTime'].dt.day
df=df.drop(['tradeTime'], axis=1)


#Delete wrong ladderRatio rows
df=df[df['ladderRatio']<10]     


#Delete 32 spezial rows
df=df.drop(df[df.drop(['buildingType', 'communityAverage'], axis=1).isnull().any(axis=1)].index, axis=0)


#traslate chinese and fill the translation in a new column
translationDict = {}
translationDict["高 "] = 1 #"High"
translationDict["中 "] = 2 #"Medium"
translationDict["底 "] = 3 #"Bottom"
translationDict["低 "] = 4 #"Low"
translationDict["顶 "] = 5 #"Top"
translationDict["未知 "] = 6 #"Unknown"
translationDict["钢混结构"] = 7 #"Steel-composite construction"
translationDict["混合结构"] = 8 #"Hybrid structure"

gbkdata['floorType'] = gbkdata['floor'].str.replace('\d+', '')  # extract chinese characters (everything but numbers)
gbkdata["floor"] = gbkdata.floor.str.extract('(\d+)')  # extract only numbers

for index_label, row_series in gbkdata.iterrows():
    # For each row update the 'floorType' value to it's translation
    gbkdata.at[index_label , 'floorType'] = translationDict[row_series['floorType']]

df.rename(columns = {'floor':'floor_old'}, inplace = True)  # rename current floor column
df.drop(['floor_old'], axis=1, inplace=True)  # delete floor_old column
df.insert(0, "floor", gbkdata["floor"])  # add new floor column to df
df.insert(0, "floorType", gbkdata["floorType"])  # add new floorType column to df


#String to cumeric
df["livingRoom"]=pd.to_numeric(df["livingRoom"], errors='coerce')
df["drawingRoom"]=pd.to_numeric(df["drawingRoom"], errors='coerce')
df["bathRoom"]=pd.to_numeric(df["bathRoom"], errors='coerce')
df["constructionTime"]=pd.to_numeric(df["constructionTime"], errors='coerce')
df["floor"]=pd.to_numeric(df["floor"], errors='coerce')
df["floorType"]=pd.to_numeric(df["floorType"], errors='coerce')


#Write csv
df.to_csv(path_or_buf='pre_cleand.csv', sep=';')