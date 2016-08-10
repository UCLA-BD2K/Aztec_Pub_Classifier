from abc import ABCMeta, abstractmethod

import tensorflow as tf
import numpy as np

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


class Classification:
    # feature_list: a list of feature functions
    # dataset: a list of data/samples
    def __init__(self, feature_list, dataset):
        self.features = feature_list
        self.dataset = dataset


    def buildFeatures(self):
        all_feature_vector = None
        labels = None

        for data in self.dataset:
            feature_vector = []
            for feat in self.features:
                feature_vector = feature_vector+feat.getFeature(data)
            if all_feature_vector is None:
                all_feature_vector = np.array([np.asarray(feature_vector)])
                labels = np.array([toBinary(data['is_tool'])])
            else:
                all_feature_vector = np.vstack((all_feature_vector, np.asarray(feature_vector)))
                labels = np.vstack((labels, np.array([toBinary(data['is_tool'])])))



        return all_feature_vector, labels

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

    def setInputDataSize(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY

    # TODO: fix function
    def runLogisticReg(self, trainX, trainY, testX, testY):
        # tf graph input
        x = tf.placeholder(tf.float32, [None, self.sizeX])
        y = tf.placeholder(tf.float32, [None, self.sizeY])

        # set model weights
        W = tf.Variable(tf.zeros([self.sizeX, self.sizeY]))
        b = tf.Variable(tf.zeros([1, self.sizeY]))

        # construct model
        pred = tf.nn.softmax(tf.matmul(x, W)+b)

        # minimize error using cross entropy
        cost = tf.reduce_mean(-tf.reduce_sum(y*tf.log(pred)))
        # gradient descent
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate).minimize(cost)

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
                    _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})

                    avg_cost += c/total_batch
                if (epoch+1)%self.display_rate == 0:
                    print("Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost))

            print("Optimization Finished!")

            # Test model
            correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
            # calculate accuracy for test set
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            print("Accuracy:", accuracy.eval({x:testX, y:testY}))
