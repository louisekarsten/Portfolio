from collections import Counter
from graphviz import Digraph
import numpy as np
import itertools

class ID3DecisionTreeClassifier:

    # Initialize the tree
    def __init__(self, minSamplesLeaf=1, minSamplesSplit=2):
        self.__nodeCounter = 0
        
        # The graph to visualise the tree
        self.__dot = Digraph(comment='The Decision Tree')
        self.__minSamplesLeaf = minSamplesLeaf
        self.__minSamplesSplit = minSamplesSplit
        
        # Attributes of the classifier to handle training parameters
        self.root = {}
        self.common = 0
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

    # Create a new node in the tree with the suggested attributes for the visualisation.
    # It can later be added to the graph with the respective function
    def new_ID3_node(self):
        node = {'id': self.__nodeCounter, 'value': None, 'label': None, 'attribute': None, 'entropy': None, 'samples': None,
                         'classCounts': None, 'nodes': list()}
        self.__nodeCounter += 1
        return node

    # Adds the node into the graph for visualisation (creates a dot-node)
    def add_node_to_graph(self, node, parentid=-1):
        nodeString = ''
        for k in node:
            if ((node[k] != None) and (k != 'nodes')):
                nodeString += "\n" + str(k) + ": " + str(node[k])

        self.__dot.node(str(node['id']), label=nodeString)
        if (parentid != -1):
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
        attributes = self.attributes
        classes = self.classes
        target = self.target
        data = self.data

        # Entropy for each attribute
        attr_entr = {}
        # Attribute is key, for example color,size or column for digits
        for attr in attributes:
            attr_entr[attr] = 0

        nbrClasses = len(classes)
        term = []
        amountClasses = []
        for j in range(0, nbrClasses):
            amountClasses.insert(j, target.count(classes[j]))
        for i in range(0, nbrClasses):
            if amountClasses[i] != 0:
                prob = amountClasses[i]*1.0 / len(data)
                term.insert(i, prob * np.log2(prob))
        I_S = -sum(term)

        term = []
        amountValues = []
        prob = []
        data_list = list(itertools.chain(*data))
        for key in attributes:
            subsets = attributes.get(key)
            nbrValues = len(subsets)
            I_Sv = []
            for j in range(0, nbrValues):
                countClasses = []
                for a in range(0,len(classes)):
                    countClasses.insert(a, 0)
                counter = data_list.count(subsets[j])
                amountValues.insert(j, counter)
                if subsets[j] in data_list:
                    dataindex = 0
                    data_index = []
                    for element in data:
                        if subsets[j] in element:
                            data_index.insert(dataindex, 1)
                        else:
                            data_index.insert(dataindex, 0)
                        dataindex = dataindex + 1
                    dataindex = 0
                    for dataindex, element in enumerate(data_index):
                        if element == 1:
                            for klass in range(0,len(classes)):
                                if target[dataindex] == classes[klass]:
                                    countClasses[klass] = countClasses[klass] + 1
                for k in range(0, len(classes)):
                    if amountValues[j] != 0:
                        prob.insert(k, countClasses[k]*1.0 / amountValues[j]*1.0)
                        if prob[k] != 0:
                            term.insert(k, prob[k] * np.log2(prob[k]))
                I_Sv.insert(j, -sum(term))
                term = []
            probnew = []
            for i in range(0, nbrValues):
                if amountValues[i] != 0:
                    probnew.insert(i, amountValues[i]*1.0 / len(target))
            prob = []
            amountValues = []
            attr_entr[key] = I_S - sum([a*b for a, b in zip(I_Sv, probnew)])
        entropy1 = I_S
        entropy2 = I_Sv
        best_attr = sorted(attr_entr, key=attr_entr.get, reverse=True)[0]
        return [best_attr, entropy1, entropy2]

    def fit(self, data, target, attributes, classes):
        self.attributes = attributes
        self.target = target
        self.classes = classes
        self.data = data
        root = self.new_ID3_node()
        root.update({'label': None, 'attribute': None, 'entropy': None, 'samples': len(target),
                     'classCounts': Counter(target).most_common(), 'nodes': []})

        if len(target) == 0:
            root.update({'label': self.common, 'entropy': 0})
            self.add_node_to_graph(root)
            self.root = root
            return root

        if target.count(target[0]) == len(target):
            common = Counter(target).most_common()[0][0]
            root.update({'label': common, 'entropy': 0, 'classCounts': common})
            self.add_node_to_graph(root)
            self.root = root
            return root

        if len(attributes) == 0:
            common = Counter(target).most_common()[0][0]
            root.update({'label': common, 'classCounts': common})
            self.add_node_to_graph(root)
            self.root = root
            return root

        A, entropy1, entropy2 = self.find_split_attr()
        root.update({'attribute': A, 'entropy': entropy1})

        newAttr = attributes.copy()
        newAttr.pop(A)
        nbr = len(attributes[A])
        attribute_index = list(attributes).index(A)
        datasplit = []
        targetsplit = []
        for n in range(nbr):
            newData = []
            targetvector = []
            for i in range(len(data)):
                if data[i][attribute_index] == attributes[A][n]:
                    datalist = list(data[i])
                    datalist.remove(data[i][attribute_index])
                    tup = tuple(datalist)
                    newData.append(tup)
                    targetvector.append(target[i])
            datasplit.append(newData)
            targetsplit.append(targetvector)

        common = Counter(target).most_common()
        self.common = common[0][0]
        self.add_node_to_graph(root)

    # Predict function
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
               
