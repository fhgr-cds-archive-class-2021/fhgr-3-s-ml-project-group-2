import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from libs import transformers as andre_transformers

df = pd.read_csv('../beijing.csv', encoding="gbk")
df.drop(columns=['id', 'url'], inplace=True)

label = "totalPrice"
X_train, X_test, Y_train, Y_test = train_test_split(df.drop(label, axis=1), df[label], test_size=0.2, random_state=42)
pipe = Pipeline([
    ('preprocessing', andre_transformers.get_preprocessing()),
])
X_train_transformed = pipe.fit_transform(X_train)
X_test_transformed = pipe.fit_transform(X_test)

# pipeline to dataframe
X_train_d = pd.DataFrame(X_train_transformed)

print(X_train_d)
print(X_train)
