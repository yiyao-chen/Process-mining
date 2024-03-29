import pygraphviz as pgv
import reader

MSG_IDX = 3

transitionMatrix = dict()
activityCount = dict()
G = pgv.AGraph(strict=False, directed=True)

mapping = {"The steady-state has deviated, a weakness may have been discovered": "The steady-state has deviated",
               "Steady state probe 'checking battery level' is not in the given tolerance so failing this experiment": "Not in the given tolerance",
               "Running experiment: Modify Sensor Battery Level/ Message-interval": "Running experiment"
               }

def getActivityCount():
    for caseId in reader.log:
        for activity in reader.log[caseId]:
            if activity[MSG_IDX] not in activityCount:
                activityCount[activity[MSG_IDX]] = 0
            activityCount[activity[MSG_IDX]] += 1


def generateGraph(activityCount):
    G = pgv.AGraph(strict=False, directed=True)
    G.graph_attr['rankdir'] = 'TB'
    G.node_attr['shape'] = 'box'

    addNodes(G, activityCount)
    addEdges(G)

    G.draw('graph.png', prog='dot')
    # print(G.string())


def addEdges(G):
    values = [transitionMatrix[ai][aj] for ai in transitionMatrix for aj in transitionMatrix[ai]]  # list comprehension
    x_min = min(values)
    x_max = max(values)
    y_min = 1.0
    y_max = 5.0
    for ai in transitionMatrix:
        for aj in transitionMatrix[ai]:
            x = transitionMatrix[ai][aj]  # transition count
            y = y_min + (y_max - y_min) * (x - x_min) / (x_max - x_min)  # edge thickness
            G.add_edge(ai, aj, label=transitionMatrix[ai][aj], penwidth=y)


def addNodes(G, activityCount):
    x_min = min(activityCount.values())
    x_max = max(activityCount.values())

    for activity in activityCount:
        text = activity + '\n count: ' + str(activityCount[activity])
        if activity.strip() in mapping.keys():
            text = mapping[activity.strip()] + '\n Count: ' + str(activityCount[activity])
        grayLevel = int(float(x_max - activityCount[activity]) / float(x_max - x_min) * 100.)
        fillColor = getFillColor(grayLevel)
        fontColor = getFontColor(grayLevel)
        G.add_node(activity, label=text, style='filled', fillcolor=fillColor, fontcolor=fontColor)


def getFontColor(grayLevel):
    fontColor = 'black'
    if grayLevel < 50:
        fontColor = 'white'
    return fontColor


def getFillColor(grayLevel):
    fillColor = 'gray' + str(grayLevel)
    return fillColor


def getActivity(caseId, taskNumber):
    return reader.log[caseId][taskNumber][MSG_IDX]


def incrementTransitionCount(fromNode, toNode):
    transitionMatrix[fromNode][toNode] += 1


def getTransitionMatrix():
    for caseId in reader.log:
        for i in range(len(reader.log[caseId]) - 1):
            ai = getActivity(caseId, i)
            aj = getActivity(caseId, i + 1)
            if ai not in transitionMatrix:
                transitionMatrix[ai] = dict()
            if aj not in transitionMatrix[ai]:
                transitionMatrix[ai][aj] = 0
            incrementTransitionCount(ai, aj)


def printTransitionMatrix():
    for ai in sorted(transitionMatrix.keys()):
        for aj in sorted(transitionMatrix[ai].keys()):
            print(ai, '-->', aj, ':', transitionMatrix[ai][aj])


def printActivityCount():
    for activity in sorted(activityCount.keys()):
        print(activity, ' count:', activityCount[activity])
