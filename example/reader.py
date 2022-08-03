import datetime

file = open("../data/event log.csv", "r")
log = dict()

def readFile():
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        parts = line.split(";")
        caseId = parts[0]
        task = parts[1]
        user = parts[2]
        timestamp = datetime.datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S")
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