import pandas as pd

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

    original_data['floorType'] = original_data['floor'].str.replace('\d+', '')  # extract chinese characters (everything but numbers)
    original_data["floor"] = original_data.floor.str.extract('(\d+)')  # extract only numbers

    for index_label, row_series in original_data.iterrows():
        # For each row update the 'floorType' value to it's translation
        original_data.at[index_label , 'floorType'] = translationDict[row_series['floorType']]

    df.rename(columns = {'floor':'floor_old'}, inplace = True)  # rename current floor column
    df.drop(['floor_old'], axis=1, inplace=True)  # delete floor_old column
    df.insert(0, "floor", original_data["floor"])  # add new floor column to df
    df.insert(0, "floorType", original_data["floorType"])  # add new floorType column to df


    #String to cumeric
    df["livingRoom"]=pd.to_numeric(df["livingRoom"], errors='coerce')
    df["drawingRoom"]=pd.to_numeric(df["drawingRoom"], errors='coerce')
    df["bathRoom"]=pd.to_numeric(df["bathRoom"], errors='coerce')
    df["constructionTime"]=pd.to_numeric(df["constructionTime"], errors='coerce')
    df["floor"]=pd.to_numeric(df["floor"], errors='coerce')
    df["floorType"]=pd.to_numeric(df["floorType"], errors='coerce')


    #Write csv
    df.to_csv(path_or_buf='data/01_pre_cleaned.csv', sep=';', index=False)

    return df
