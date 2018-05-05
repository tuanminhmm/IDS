# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import os
import sys
import traceback
import weka.core.jvm as jvm
#import Helper as helper
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation
from weka.filters import Filter
from weka.clusterers import Clusterer, ClusterEvaluation, FilteredClusterer


class wekaTrainTest:
	def __init__ (self, datasetName, dataTestName):
		#datasetName: name of the data set will be import to train (.arff format)
		#sataTestName: name of data will be evaluate (.arff format)
		if len(datasetName) <=1:
			self.datasetName = helper.get_data_dir() + os.sep + "KDDTrain+.arff"
		else:
			self.datasetName = datasetName
		self.dataTestName = dataTestName


	# train data set	
	def train_data(self):
		try:
			#helper.print_info("Loading dataset: " + self.datasetName)
			loader = Loader(classname="weka.core.converters.ArffLoader")
			data_train = loader.load_file(self.datasetName)
			data_train.delete_last_attribute()
			clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "2"])
			clusterer.build_clusterer(data_train)
			return clusterer

		except Exception, e:
			raise e
			print(traceback.format_exc())


	#evaluate data
	def evaluation_data(self, model):
		try:
			loader = Loader(classname="weka.core.converters.ArffLoader")
			data_test = loader.load_file(self.dataTestName)
			#helper.print_info("Evaluating on data:")
			evaluation = ClusterEvaluation()

			evaluation.set_model(model)
			evaluation.test_model(data_test)
			#print("# clusters: " + str(evaluation.num_clusters))
			#print("# log likelihood: " + str(evaluation.log_likelihood))
			cluster_ass = evaluation.cluster_assignments
			#print("# cluster assignments:\n" + str(cluster_ass))
			f = open("result_data.txt","w+")
			i = 0
			for ins in data_test:
				stt = "normal"
				if(cluster_ass[i] == 0):
					stt = "anomaly"
				statement = str(ins) + "," + stt
				#print statement 
				f.write(statement + "\n")
				i = i + 1

			f.close()
			return evaluation.cluster_results
		except Exception, e:
			raise e
			print(traceback.format_exc())

	# start all function (include data set and data test above)
	def start(self):
		try:
			jvm.start()
			model = self.train_data()
			evaluated_data = self.evaluation_data(model)
			#print evaluated_data
		except Exception, e:
			pass
