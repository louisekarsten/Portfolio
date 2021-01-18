from collections import Counter
from graphviz import Digraph
import numpy as np

class ID3DecisionTreeClassifier:

    # Initialize the tree
    def __init__(self, minSamplesLeaf=1, minSamplesSplit=2):
        self.__nodeCounter = 0
        self.__dot = Digraph(comment='The Decision Tree')
        self.__minSamplesLeaf = minSamplesLeaf
        self.__minSamplesSplit = minSamplesSplit
        self.attributes = 0
        self.target = 0
        self.classes = 0
        self.data = 0
        self.target = 0
        self.parentId = 0
        self.predicted = list

    # Create a new node in the tree
    def new_ID3_node(self):
        node = {'id': self.__nodeCounter, 'value': None,
                'label': None, 'attribute': None, 'entropy': None,
                'samples': None, 'classCounts': None, 'nodes': list()}
        self.__nodeCounter += 1
        return node

    # Add a node into the graph for visualisation
    def add_node_to_graph(self, node, parentid=-1):
        nodeString = ''
        for k in node:
            if ((node[k] != None) and (k != 'nodes')):
                nodeString += "\n" + str(k) + ": " + str(node[k])
        self.__dot.node(str(node['id']), label=nodeString)
        if parentid != -1:
            self.__dot.edge(str(parentid), str(node['id']))
            nodeString += "\n" + str(parentid) + " -> " + str(node['id'])
        print(nodeString)
        return

    # Call the visualisation
    def make_dot_data(self):
        return self.__dot

    # Find the best attribute to split with, given the set of remaining attributes,
    # the currently evaluated data and target.
    def find_split_attr(self):
        target = self.target
        classes = self.classes
        data = self.data
        attributes = self.attributes
        term = []

        totentr = 0
        count_tar = {}

        for c in classes:
            count_tar[c] = 0

        for targ in target:
            count_tar[targ] += 1

        for c in classes:
            if int(count_tar[c]) != 0 & sum(list((count_tar.values()))) != 0:
                totentr += -int(count_tar[c]) / sum(list(count_tar.values())) * np.log2(
                    int(count_tar[c]) / sum(list((count_tar.values()))))

        attr_entr = {}
        for attr in attributes:
            attr_entr[attr] = 0

        for i, attr in enumerate(attributes):

            for sample in attributes[attr]:
                count_samp = {}

                for c in classes:
                    count_samp[c] = 0
                entr_samp = 0
                for j in range(len(data)):
                    if data[j][i] == sample:
                        count_samp[target[j]] += 1
                if sum(list(count_samp.values())) != 0:
                    for c in count_samp:
                        if count_samp[c] != 0 & sum(list(count_samp.values())) != 0:
                            entr_samp += -count_samp[c] / sum(list(count_samp.values())) * np.log2(
                                count_samp[c] / sum(list(count_samp.values())))

                entr_samp *= sum(list(count_samp.values())) / len(data)
                attr_entr[attr] += entr_samp
                self.entropy = attr_entr[attr]
            attr_entr[attr] = totentr - attr_entr[attr]
        best_attr = sorted(attr_entr, key=attr_entr.get, reverse=True)[0]

        return best_attr

    def get_entropy(self, count_tar, classes):
        totentr = 0
        for c in classes:
            count_tar[c] = 0
            if int(count_tar[c]) != 0 &  sum(list((count_tar.values()))) != 0:
                totentr += -int(count_tar[c]) / sum(list(count_tar.values())) * np.log2(
                    int(count_tar[c]) / sum(list((count_tar.values()))))
        return totentr

    # Recursive ID3-algorithm
    def fit(self, data, target, attributes, classes):
        self.attributes = attributes
        self.classes = classes
        self.data = data
        self.target = target
        root = self.new_ID3_node()
        root.update({'label': None, 'attribute': None, 'entropy': self.get_entropy(dict(Counter(target)), classes),
                     'samples': len(target),
                     'classCounts': Counter(target).most_common(), 'nodes': []})
        counter = 0
        if len(target) == 0:
            root.update({'label': self.mostc})
            self.add_node_to_graph(root)
            self.root = root
            return root

        if target.count(target[0]) == len(target):
            mostcommon = Counter(target).most_common()
            root.update({'label': mostcommon[0][0]})
            root.update({'entropy': 0})
            root.update({'classCounts': mostcommon})
            self.add_node_to_graph(root)
            self.root = root
            return root

        if len(attributes) == 0:
            mostcommon = Counter(target).most_common()
            root.update({'label': mostcommon[0][0]})
            self.add_node_to_graph(root)
            self.root = root
            return root
        else:
            splitattribute = self.find_split_attr()
            root.update({'entropy': self.entropy})
            newattributes = attributes.copy()
            newattributes.pop(splitattribute)
            root.update({'attribute': splitattribute})

            # Length of data
            l = len(data)
            # Number of different values in attribute
            nbr = len(attributes[splitattribute])
            # Index of attribute
            attribute_index = list(attributes).index(splitattribute)
            # Splitted data
            datasplit = []
            targetsplit = []

            for n in range(nbr):
                templist = []
                temptarget = []
                for i in range(l):
                    # If the data at index(i,attribute) == value at attribute
                    if data[i][attribute_index] == attributes[splitattribute][n]:
                        tlist = list(data[i])
                        tlist.remove(data[i][attribute_index])
                        tup = tuple(tlist)
                        templist.append(tup)
                        temptarget.append(target[i])
                datasplit.append(templist)
                targetsplit.append(temptarget)

            mostcommon = Counter(target).most_common()
            self.mostc = mostcommon[0][0]
            self.add_node_to_graph(root)
            for n in range(nbr):
                child = self.fit(datasplit[n], targetsplit[n], newattributes, classes)
                val = attributes[splitattribute][n]
                root['nodes'].append(child)
                child.update({'value': val})
                self.add_node_to_graph(child, root['id'])
            self.root = root
            return root

    # Predict the
    def predict(self, data, tree, attributes):
        self.attributes = attributes
        predicted = list()
        for d in data:
            predicted.append(self.predictrec(d, tree))
        return predicted

    # Recursive predict method
    def predictrec(self, data, tree):
        if tree['label'] != None:  # node is leaf:
            return tree['label']
        # find the child c among the children of node representing
        # the value that x has for the split_attribute of node
        else:
            attr = tree['attribute']
            children = tree['nodes']
            for child in children:
                for i, at in enumerate(self.attributes):
                    if attr == at:
                        datavalue = data[i]
                        if child['value'] == datavalue:
                            return self.predictrec(data, child)