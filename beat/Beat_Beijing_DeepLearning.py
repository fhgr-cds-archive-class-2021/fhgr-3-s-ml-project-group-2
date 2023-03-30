# %%
import pandas as pd
import tensorflow as tf
import kerastuner as keras_tuner
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras.utils.vis_utils import plot_model
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

# %%
train = pd.read_csv("train.csv",encoding="gbk", low_memory=False, delimiter=';')
test = pd.read_csv("test.csv",encoding="gbk", low_memory=False, delimiter=';')
train.where(train["totalPrice"]>3000).dropna()
x_train = train.drop(['totalPrice'], axis=1)
y_train = train['totalPrice']
x_test = train.drop(['totalPrice'], axis=1)
y_test = train['totalPrice']
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.33, shuffle= True)
print("Input shape: "+str(x_train.shape[1]))

normalization_layer= tf.keras.layers.Normalization()
normalization_layer.adapt(x_train)

# %%

def build_model(hp=keras_tuner.HyperParameters()):
    model = tf.keras.models.Sequential()
    model.add(normalization_layer)
    model.add(tf.keras.layers.Dense(
                            hp.Int("units1", min_value=50, max_value=600, step=50), 
                            input_dim=26, 
                            activation=hp.Choice("activation1", ["relu", "tanh"])))
    

    for i in range(hp.Int('num_layers', 2, 20)):
        #if hp.Boolean('dropout'+str(i)):
            #model.add(tf.keras.layers.Dropout(rate=0.25))
        
        model.add(tf.keras.layers.Dense(
                                    hp.Int("units"+str(i), min_value=50, max_value=600, step=50),
                                    activation=hp.Choice("activation"+str(i), ["relu", "tanh"])))
                                    
    
    model.add(tf.keras.layers.Dense(1, activation='linear'))
    model.compile(
                optimizer=hp.Choice('optimizer', ["adam", "SGD", "Adadelta" , "Adamax"]),
                loss=tf.keras.losses.MeanAbsoluteError(), 
                metrics=tf.keras.metrics.MeanAbsoluteError())
    
    return model

print(build_model())



callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)

tuner = keras_tuner.RandomSearch(
    hypermodel=build_model,
    objective=keras_tuner.Objective("val_mean_absolute_error", direction="min"),
    max_trials=3,
    overwrite=True,
    directory="my_dir",
    project_name="built_in_metrics",

)
tuner.search(x_train, y_train, epochs=20, validation_data=(x_valid, y_valid), callbacks=[callback])



#%%
models = tuner.get_best_models(num_models=2)
model = models[0]
model.build(input_shape=(None, 26))
print(model.summary())
plot_model(model,to_file="model.png",show_shapes=True, show_layer_activations=True)


# %%
history=model.fit(x_train,y_train,epochs=20, verbose=1, validation_data=(x_valid, y_valid), callbacks=[callback])

# %%
model.summary()
tuner.results_summary()
tuner.search_space_summary()


# %%
print("Evaluate on test data")
results = model.evaluate(x_test, y_test)
print("test loss, test mae:", results)
# %%
plt.figure(1)
plt.plot(history.history['loss'], label="loss")
plt.plot(history.history['val_loss'], label="val_loss")
plt.title("MAE")
plt.legend()

print(history.history.keys())
# %%
