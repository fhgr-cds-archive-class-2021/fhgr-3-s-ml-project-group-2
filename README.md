# Machine Learning Project - FHGR - CDS106
## Goal of the project
We have chosen following dataset from [kaggle](https://www.kaggle.com/) for our project: [Housing price in Beijing](https://www.kaggle.com/datasets/ruiqurm/lianjia). More informations about the dataset can be found on kaggle.
The goal of this project is to answer following research question:
- Can we predict the price of a Beijing residential property based on property characteristics?

The original dataset is stored here: [beijing_original.csv](/app/data/beijing_original.csv) or available on the kaggle page (link above).

## Project members
- André Glatzl (personal folder: [/andre](./andre))
- Beat Brändli (personal folder: [/beat](./beat))
- Leandro Gregorini (personal folder: [/leandro](./leandro))
- Raphael Brunold (personal folder: [/raphael](./raphael))


## Project organisation
Every project member experimented and explorated the dataset in his own folder (as linked above).
The [/nominatim](./nominatim) folder is used for the pre population step in our workflow described below.
Then we combined our collected knowledge and created the [/app](./app) folder with our **final result and ML-model**.


## How to run the machine learning workflow
Our final **results** are stored in the [/app](./app) folder.

To run the machine learning workflow the [/app/main.py](./app/main.py) script in the [/app](./app) folder has to be started.
Following subscripts are then triggered:
- [/app/_00_pre_population.py](./app/_00_pre_population.py)
  - The original dataset gets enriched with geodata from [OpenStreetMap](https://www.openstreetmap.org/) using [Nominatim](https://nominatim.org/)
- [/app/_01_pre_cleaning.py](./app/_01_pre_cleaning.py)
  - The dataset from the previous step gets cleanded: 
    - datetime split
    - delete false rows
    - delete unnecessary rows
    - translate chinese characters
    - set datatypes (in the dataframe)
- [/app/_02_pre_processing.py](./app/_02_pre_processing.py)
  - The dataset from the previous step gets preprocessed:
    - create time periods for construction time column
    - Train/Test dataset split
    - set datatpyes for categorical columns
    - empty data imputation and encoding of the data
- [/app/_03_modelling.py](./app/_03_modelling.py)
  - The dataset from the previous step is used for the machine learning algorithm:
    - Model: Stacking Regressor
- [/app/_04_interpretation.py](./app/_04_interpretation.py)
  - The machine learning model gets analyzed (scores and other important metrics)

In every step a pandas dataframe was returned from the subscripts in order to guarantee modularity.

After every step a new csv gets created and stored in the [/app/data](./app/data) folder. The ML-model is stored in the [/app/data](./app/data) folder aswell.

This helpes in the development process because a dataset of every substep is available and therefore it's not necessary to always run the whole workflow to make changes on a specific step or file. Also, this way of working allowed us to encapsulate our work from each other and reduce interdependence during development.
