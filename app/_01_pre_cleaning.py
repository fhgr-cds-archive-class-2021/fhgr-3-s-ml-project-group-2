import pandas as pd
import numpy as np

def pre_cleaning(original_data: pd.DataFrame) -> pd.DataFrame:
    
    #drop usless columns
    df = original_data.drop(['url', 'id', 'Cid', 'DOM', 'price', 'followers'], axis=1)


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


    df['floorType'] = df['floor'].copy()
    def mapper(x):
        splitted = x.split(' ')
        finalStr = x
        if len(splitted) == 2:
            finalStr = splitted[0]
        translations = {
            '中': 'middle',
            '低': 'low',
            '底': 'bottom',
            '未知': 'Unknown',
            '混合结构': 'hybrid',
            '钢混结构': 'steel',
            '顶': 'top',
            '高': 'high'
        }
        return translations[finalStr]
        
    df['floorType'] = df['floorType'].apply(mapper)

    def mapper(x):
        splitted = x.split(' ')
        if len(splitted) == 2:
            return splitted[1]
        else:
            return np.nan
    df['floor'] = df['floor'].apply(mapper)
    df['floor'] = df['floor'].astype(int)
    
    #String to cumeric
    df["livingRoom"]=pd.to_numeric(df["livingRoom"], errors='coerce')
    df["drawingRoom"]=pd.to_numeric(df["drawingRoom"], errors='coerce')
    df["bathRoom"]=pd.to_numeric(df["bathRoom"], errors='coerce')
    df["constructionTime"]=pd.to_numeric(df["constructionTime"], errors='coerce')
    df["floor"]=pd.to_numeric(df["floor"], errors='coerce')
    df["buildingType"]=pd.to_numeric(df["buildingType"], errors='coerce')

    #Write csv
    df.to_csv(path_or_buf='data/01_pre_cleaned.csv', sep=';', index=False)

    return df

#df= pd.read_csv("C:\\Users\\beatb\\OneDrive\\Documents\\5. Semester\\Maschine_Learning\\Projekt\\fhgr-3-s-ml-project-group-2\\beat\\beijing_original.csv",encoding="gbk", low_memory=False)
#x=pre_cleaning(df)
