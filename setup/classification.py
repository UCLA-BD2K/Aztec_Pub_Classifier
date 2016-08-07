from abc import ABCMeta, abstractmethod

class Feature:
    __metaclass__ = ABCMeta
    @abstractmethod
    def getFeature(self, obj):
        raise NotImplementedError()

    def toBinary(self, value):
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
        feature_vector = []
        for sample in self.dataset:
            sample_vector = []
            for feature in self.features:
                sample_vector.append(feature.getFeature(sample))
            feature_vector.append(sample_vector)

        return feature_vector

        # TODO: input classification function
        # features: a list of feature vectors
        # output: a list of classifications
        def classify(self, features):
            cl_vector = []

            # TODO: fill in code to classify dataset


            return cl_vector
