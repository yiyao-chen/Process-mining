import pygraphviz as pgv

file = open("data/event log.csv", "r")
#
# log = []
#
# for line in file:
#     line = line.strip()
#     if len(line) == 0:
#         continue
#     parts = line.split(";")
#     caseId = parts[0]
#     task = parts[1]
#     user = parts[2]
#     timestamp = parts[3]
#     event = (caseId, task, user, timestamp)
#     log.append(event)
#
# log.sort(key=lambda event: (event[0], event[3]))
# for (caseId, task, user, timestamp) in log:
#    print(caseId, task, user, timestamp)

log = dict()
transitionMatrix = dict()
activityCount = dict()

def main():
    readFile()
    sortLog()
    getControlFlow()
    printControlFlow()

    getActivityCount()

    print('Activity count:')
    for activity in sorted(activityCount.keys()):
        print(activity, ' count:', activityCount[activity])

    generateGraph(activityCount)


def getActivityCount():
    for caseId in log:
        for activity in log[caseId]:
            if activity[0] not in activityCount:
                activityCount[activity[0]] = 0
            activityCount[activity[0]] += 1


def generateGraph(activityCount):
    G = pgv.AGraph(strict=False, directed=True)
    G.graph_attr['rankdir'] = 'LR'
    G.node_attr['shape'] = 'box'

    addNodes(G, activityCount)
    addEdges(G)

    G.draw('graph.png', prog='dot')
    #print(G.string())


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
    print(x_min, x_max)

    for activity in activityCount:
        text = activity + '\n count: ' + str(activityCount[activity])
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


def readFile():
    # global log, caseId, task, user, timestamp
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        parts = line.split(";")
        caseId = parts[0]
        task = parts[1]
        user = parts[2]
        timestamp = parts[3]
        if caseId not in log:
            log[caseId] = []
        event = (task, user, timestamp)
        log[caseId].append(event)
    file.close()


def sortLog():
    for caseId in sorted(log.keys()):
        log[caseId].sort(key=lambda event: event[-1])  # sort by timestamp
        for (task, user, timestamp) in log[caseId]:
            print(caseId, task, user, timestamp)


def getActivity(caseId, taskNumber):
    return log[caseId][taskNumber][0]


def incrementTransitionCount(fromNode, toNode):
    transitionMatrix[fromNode][toNode] += 1


def getControlFlow():
    # global caseId, ai, aj
    for caseId in log:
        for i in range(len(log[caseId]) - 1):
            ai = getActivity(caseId, i)
            aj = getActivity(caseId, i + 1)
            if ai not in transitionMatrix:
                transitionMatrix[ai] = dict()
            if aj not in transitionMatrix[ai]:
                transitionMatrix[ai][aj] = 0
            incrementTransitionCount(ai, aj)


def printControlFlow():
    for ai in sorted(transitionMatrix.keys()):
        for aj in sorted(transitionMatrix[ai].keys()):
            print(ai, '-->', aj, ':', transitionMatrix[ai][aj])


if __name__ == '__main__':
    main()
