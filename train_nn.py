import tensorflow as tf
import numpy as np

TRAINING_DATA = "train.csv"
TEST_DATA = "test.csv"

training_set = tf.contrib.learn.datasets.base.load_csv(filename=TRAINING_DATA, target_dtype=np.int)
test_set = tf.contrib.learn.datasets.base.load_csv(filename=TEST_DATA, target_dtype=np.int)

x_train, x_test, y_train, y_test = training_set.data, test_set.data, \
  training_set.target, test_set.target

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(hidden_units=[1000, 1000], n_classes=2)

# Fit model.
classifier.fit(x=x_train, y=y_train, steps=1000)

# Evaluate accuracy.
accuracy_score = classifier.evaluate(x=x_test, y=y_test)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))