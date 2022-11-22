# libraries
import pandas as pd
import os
import numpy as np


# create new column with period label -> src: https://towardsdatascience.com/how-to-group-yearly-data-by-periods-5199a1dba5db
def createYearPeriods(df, columnName, periodLength=10):
    df[columnName] = df[columnName].astype('Int64')

    startYear = df[columnName].min()
    endYear = df[columnName].max()
    yearRange = endYear - startYear
    modulo = yearRange % periodLength

    if modulo == 0:
        finalStart = endYear - periodLength
    else:
        finalStart = endYear - modulo
    finalEnd = endYear+1

    starts = np.arange(startYear, finalStart, periodLength).tolist()
    tuples = [(start, start+periodLength) for start in starts]
    tuples.append(tuple([finalStart, finalEnd]))
    bins = pd.IntervalIndex.from_tuples(tuples, closed='left')

    originalLabels = list(bins.astype(str))
    newLabels = ['{} - {}'.format(b.strip('[)').split(', ')[0], int(b.strip('[)').split(', ')[1])-1) for b in originalLabels]
    label_dict = dict(zip(originalLabels, newLabels))

    periodColumnName = str(columnName) + 'Period'
    # Assign each row to a period
    df[periodColumnName] = pd.cut(df[columnName], bins=bins, include_lowest=True, precision=0)
    df[periodColumnName] = df[periodColumnName].astype("str")
    df = df.replace(label_dict)

    return df