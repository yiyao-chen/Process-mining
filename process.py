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
controlFlow = dict()


def main():
    readFile()
    sortLog()
    getControlFlow()
    printControlFlow()


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
    controlFlow[fromNode][toNode] += 1


def getControlFlow():
    # global caseId, ai, aj
    for caseId in log:
        for i in range(len(log[caseId]) - 1):
            ai = getActivity(caseId, i)
            aj = getActivity(caseId, i + 1)
            if ai not in controlFlow:
                controlFlow[ai] = dict()
            if aj not in controlFlow[ai]:
                controlFlow[ai][aj] = 0
            incrementTransitionCount(ai, aj)


def printControlFlow():
    for ai in sorted(controlFlow.keys()):
        for aj in sorted(controlFlow[ai].keys()):
            print(ai, '-->', aj, ':', controlFlow[ai][aj])


if __name__ == '__main__':
    main()
