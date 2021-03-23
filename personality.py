from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import itertools

import pandas as pd
import numpy as np
import tensorflow as tf

tf.logging.set_verbosity(tf.logging.INFO)

COLUMNS = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6",
           "Q7", "Q8", "Q9", "Q10", "gender", "age", "personality"]
FEATURES = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6",
            "Q7", "Q8", "Q9", "Q10", "gender", "age"]
LABEL = "personality"


def input_fn(data_set):
  feature_cols = {k: tf.constant(data_set[k].values) for k in FEATURES}
  labels = tf.constant(data_set[LABEL].values)
  return feature_cols, labels



def main():
  # Load datasets
  training_set = pd.read_csv("training.csv", skipinitialspace=True,
                             skiprows=1, names=COLUMNS)
  test_set = pd.read_csv("test.csv", skipinitialspace=True,
                         skiprows=1, names=COLUMNS)


  # Passing user's input
  prediction_set = pd.read_csv("prediction.csv", skipinitialspace=True,
                               skiprows=1, names=COLUMNS)

  # Feature cols
  feature_cols = [tf.contrib.layers.real_valued_column(k)
                  for k in FEATURES]

  # Build 2 layer fully connected DNN with 13, 13 units respectively.
  regressor = tf.contrib.learn.DNNRegressor(feature_columns=feature_cols,
                                            hidden_units=[13, 13],
                                           model_dir="trained_values/")

  # Fit
  regressor.fit(input_fn=lambda: input_fn(training_set), steps=5000)


  # Score accuracy
  ev = regressor.evaluate(input_fn=lambda: input_fn(test_set), steps=1)
  loss_score = ev["loss"]
  print("Loss: {0:f}".format(loss_score))

 # Print out predictions
  y = regressor.predict(input_fn=lambda: input_fn(prediction_set))


  # .predict() returns an iterator; convert to a list and print predictions

  prediction = list(itertools.islice(y, 1))
  return prediction