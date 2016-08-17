from abc import ABCMeta, abstractmethod

import tensorflow as tf
import sklearn.metrics as sk
import sklearn.svm  as svm
import numpy as np
from time import sleep
from enum import Enum
from sklearn.cross_validation import train_test_split


ABSTRACT_THRESHOLD = 200

class ML_Method(Enum):
    LR = 1
    SVM = 2
    NN = 3

class Feature:
    __metaclass__ = ABCMeta
    @abstractmethod
    def getFeature(self, obj):
        raise NotImplementedError()

def toBinary(value):
    if value is True:
        return 1
    else:
        return 0

def one_hot(value):
    if value is True:
        return [0, 1]
    else:
        return [1, 0]

class Classification:
    # feature_list: a list of feature functions
    # dataset: a list of data/samples
    def __init__(self, feature_list, dataset):
        (self.all_features, self.labels) = self.buildFeatures(feature_list, dataset)



    def buildFeatures(self, features, dataset):
        all_feature_vector = None
        labels = None

        for data in dataset:
            feature_vector = []

            if len(data['abstract']) > ABSTRACT_THRESHOLD:

                for feat in features:
                    feature_vector = feature_vector+feat.getFeature(data)
                if all_feature_vector is None:
                    all_feature_vector = np.array([np.asarray(feature_vector)])
                    labels = np.array([one_hot(data['is_tool'])])
                else:
                    all_feature_vector = np.vstack((all_feature_vector, np.asarray(feature_vector)))
                    labels = np.vstack((labels, np.array([one_hot(data['is_tool'])])))

        return all_feature_vector, labels

    def train(self, method, learning_rate, epochs, batch):
        trainer = Trainer(learning_rate, epochs, batch, batch)
        if method == ML_Method.LR:
            X_train, X_test, y_train, y_test = train_test_split(self.all_features, self.labels, test_size=0.6)
            trainer.runLogisticReg(X_train, y_train, X_test, y_test)
        elif method == ML_Method.SVM:
            one_hot_y = [l[1] for l in self.labels]
            X_train, X_test, y_train, y_test = train_test_split(self.all_features, one_hot_y, test_size=0.6)
            trainer.runSVM(X_train, y_train, X_test, y_test)


    # TODO: input classification function
    # features: a list of feature vectors
    # output: a list of classifications
    def classify(self, features):
        cl_vector = []

        # TODO: fill in code to classify dataset


        return cl_vector

class Trainer:
    def __init__(self, learning_rate, epochs, batch, display_rate):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch = batch
        self.display_rate = display_rate
        self.sizeX = 0
        self.sizeY = 0


    def runLogisticReg(self, trainX, trainY, testX, testY):
        # tf graph input
        sizeX = len(trainX[0])
        sizeY = len(trainY[0])
        x = tf.placeholder(tf.float32, [None, sizeX])
        y = tf.placeholder(tf.float32, [None, sizeY])

        #rate = tf.train.exponential_decay(learning_rate=self.learning_rate,
        #                                  global_step=1, decay_steps=trainX.shape[0],
        #                                  decay_rate=0.95, staircase=True)

        # set model weights
        W = tf.Variable(tf.random_normal([sizeX, sizeY]))
        b = tf.Variable(tf.random_normal([1, sizeY]))

        # construct model
        pred = tf.nn.softmax(tf.matmul(x, W)+b)

        # minimize error using cross entropy
        #cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(tf.clip_by_value(pred,1e-10,1.0))))
        cost = tf.nn.l2_loss(pred-y)
        # gradient descent
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(cost)

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # calculate accuracy
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        # initialize all variables
        init = tf.initialize_all_variables()

        # launch graph, train model
        trainLen = len(trainX)
        with tf.Session() as sess:
            sess.run(init)

            for epoch in range(self.epochs):
                avg_cost = 0.
                total_batch = int(trainLen/self.batch)

                for i in range(total_batch):
                    start_in = i*self.batch
                    end_in = start_in + self.batch
                    batch_xs = trainX[start_in : end_in]
                    batch_ys = trainY[start_in : end_in]
                    step, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})
                    avg_cost += c/total_batch
                if (epoch+1)%self.display_rate == 0:
                    acc = accuracy.eval({x: trainX, y: trainY})
                    print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost), "accuracy=", acc)



            print("Optimization Finished!")
            y_p = tf.argmax(pred, 1)
            val_accuracy, y_pred = sess.run([accuracy, y_p], feed_dict={x:testX, y:testY})

            print("validation accuracy:", val_accuracy)
            y_true = np.argmax(testY,1)
            print("Precision", sk.precision_score(y_true, y_pred))
            print("Recall", sk.recall_score(y_true, y_pred))
            print("f1_score", sk.f1_score(y_true, y_pred))
            print(sk.classification_report(y_true, y_pred))
            print("confusion_matrix")
            print(sk.confusion_matrix(y_true, y_pred))

    def runSVM(self, trainX, trainY, testX, testY):
        clf = svm.SVC(gamma=0.001, C=50, max_iter=400000)
        clf.fit(trainX, trainY)
        y = clf.predict(testX)
        print(clf.score(testX, testY))
        print(sk.classification_report(testY, y))
        print(sk.confusion_matrix(testY, y))
