# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# train_test_split.py
# Copyright (C) 2015 Fracpete (pythonwekawrapper at gmail dot com)

import os
import sys
import traceback
import weka.core.jvm as jvm
import Helper as helper
from weka.core.classes import Random
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation
from weka.filters import Filter
#from weka.core import Drawable
#import weka.plot.clusterers as plc


def main(args):
    """
    Loads a dataset, shuffles it, splits it into train/test set. Trains J48 with training set and
    evaluates the built model on the test set.
    :param args: the commandline arguments (optional, can be dataset filename)
    :type args: list
    """

    # load a dataset
    if len(args) <= 1:
        data_file = helper.get_data_dir() + os.sep + "KDDTrain+_20Percent.arff"
        #data_file2 = helper.get_data_dir() + os.sep + "KDDTest-21.arff"
    else:
        data_file = args[1]
        #data_file2 = args[1]
    helper.print_info("Loading dataset: " + data_file)
    loader = Loader(classname="weka.core.converters.ArffLoader")
    data = loader.load_file(data_file)
    data_test = loader.load_file("cc_5attr.arff")
    data.delete_last_attribute()
    #data_test.delete_last_attribute()
    #data.class_is_last()

    # generate train/test split of randomized data
   # train, test = data.train_test_split(66.0, Random(1))

    

    from weka.clusterers import Clusterer, ClusterEvaluation, FilteredClusterer

    clusterer = Clusterer(classname="weka.clusterers.SimpleKMeans", options=["-N", "2"])
    clusterer.build_clusterer(data)

    print("DONE!")
    #print(clusterer.capabilities)

    helper.print_info("Evaluating on data")
    evaluation = ClusterEvaluation()
    #string_result = evaluation.evaluateClusterer(clusterer, options=["-T", data_test])
    evaluation.set_model(clusterer)
    evaluation.test_model(data_test)
    print("# clusters: " + str(evaluation.num_clusters))
    print("# log likelihood: " + str(evaluation.log_likelihood))
    print("# cluster assignments:\n" + str(evaluation.cluster_assignments))

    #print("Evaluation:\n" + string_result)
    
    print("Result:\n")
    print(evaluation.cluster_results)
    print("================================AHIHI==========================================")

    remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    fclusterer = FilteredClusterer()
    fclusterer.clusterer = clusterer
    fclusterer.filter = remove
    fclusterer.build_clusterer(data)
    print(fclusterer)
    
    #clusterer.graph()

    #cluster the data
    #for inst in evaluation.cluster_results:
    #    cl = clusterer.cluster_instance(inst)  # 0-based cluster index
    #    dist = clusterer.distribution_for_instance(inst)   # cluster membership distribution
    #    print("cluster=" + str(cl) + ", distribution=" + str(dist))

    #print("Class to cluster:\n")
    #print(evaluation.classes_to_clusters)
    #print(clusterer.graph)
    #plc.plot_cluster_assignments(evaluation, data, inst_no=True)

     # partial classname
    #helper.print_title("Creating clusterer from partial classname")
    #clsname = ".SimpleKMeans"
    #clusterer = Clusterer(classname=clsname)
    #print(clsname + " --> " + clusterer.classname)


    
    #data.class_is_last()
    # build classifier
    #cls = Classifier(classname="weka.classifiers.trees.J48")
    #cls.build_classifier(data)
    #print(cls)

    #print("=========================================================================")

    # evaluate
    #evl = Evaluation()
    #evl.test_model(cls, data_test)
    #print(evl.summary())


    #print("=================== TIME TO DO IT =======================")
    #remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "last"])
    #remove.inputformat(data_test)
    #data_filtered = remove.outputformat()
    #clusterer.build_clusterer(data_test)
    #for inst in loader:
        #remove.input(inst)
        #inst_filtered = remove.output()
        #clusterer.update_clusterer(inst)
    #clusterer.update_finished()
    #print(clusterer)



if __name__ == "__main__":
    try:
        jvm.start()
        main(sys.argv)
    except Exception, e:
        print(traceback.format_exc())
    finally:
        jvm.stop()