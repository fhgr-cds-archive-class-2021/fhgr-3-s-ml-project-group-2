import requests
import multiprocessing
import pandas as pd
import numpy as np

def parallel_rows(rows: pd.Series) -> pd.Series:
    URL = "http://localhost:8111/reverse?format=jsonv2&lat={}&lon={}"

    # Data Source : http://www.citypopulation.de/en/china/beijing/admin/
    metadata = {
        '东城区': {
            'translated': 'Dongcheng',
            'population': 708829,
            'area': 40.6,
        },
        '西城区': {
            'translated': 'Xicheng',
            'population': 1106214,
            'area': 46.5,
        },
        '朝阳区': {
            'translated': 'Chaoyang',
            'population': 3452460,
            'area': 470.8,
        },
        '丰台区': {
            'translated': 'Fengtai',
            'population': 2019764,
            'area': 304.2,
        },
        '石景山区': {
            'translated': 'Shijingshan',
            'population': 567851,
            'area': 89.8,
        },
        '海淀区': {
            'translated': 'Haidian',
            'population': 3133469,
            'area': 426.0,
        },
        '门头沟区': {
            'translated': 'Mentougou',
            'population': 392606,
            'area': 1331.3,
        },
        '房山区': {
            'translated': 'Fangshan',
            'population': 1312778,
            'area': 1866.7,
        },
        '通州区': {
            'translated': 'Tongzhou',
            'population': 1840295,
            'area': 870.0,
        },
        '顺义区': {
            'translated': 'Shunyi',
            'population': 1324044,
            'area': 980.0,
        },
        '昌平区': {
            'translated': 'Changping',
            'population': 2269487,
            'area': 1430.0,
        },
        '大兴区': {
            'translated': 'Daxing',
            'population': 1993591,
            'area': 1012.0,
        },
        '怀柔区': {
            'translated': 'Huairou',
            'population': 441040,
            'area': 2557.3,
        },
        '平谷区': {
            'translated': 'Pinggu',
            'population': 457313,
            'area': 1075.0,
        },
        '密云区': {
            'translated': 'Miyun',
            'population': 527683,
            'area': 2335.6,
        },
        '延庆区': {
            'translated': 'Yanqing',
            'population': 345671,
            'area': 1980.0,
        }
    }
    for index, row in rows.iterrows():
        lat = row['Lat']
        lon = row['Lng']
        response = requests.get(URL.format(lat, lon))
        data = response.json()
        placeRank = data['place_rank']
        if 'town' in data['address']:
            town = data['address']['town']
        elif 'village' in data['address']:
            town = data['address']['village']
        else:
            town = np.nan

        if 'city' in data['address']:
            district = data['address']['city']
        else:
            district = np.nan

        if district in metadata:
            districtPopulation = metadata[district]['population']
            districtArea = metadata[district]['area']
            rows.at[index, 'districtPopulation'] = districtPopulation
            rows.at[index, 'districtArea'] = districtArea

        rows.at[index, 'placeRank'] = placeRank
        rows.at[index, 'town'] = town
    return rows

def pre_population(original: pd.DataFrame) -> pd.DataFrame:
    df = original.copy()

    df["placeRank"] = np.nan
    df["town"] = np.nan
    df["districtPopulation"] = np.nan
    df["districtArea"] = np.nan

    num_cores = 6  #leave one free to not freeze machine
    num_partitions = num_cores #number of partitions to split dataframe
    chunks = np.array_split(df, num_partitions)
    pool = multiprocessing.Pool(num_cores)
    df = pd.concat(pool.map(parallel_rows, chunks))
    pool.close()
    pool.join()

    # Write csv
    df.to_csv(path_or_buf='data/00_pre_populated.csv', sep=';', index=False)
    return df
