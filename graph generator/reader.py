
file = open("../data/functional_chaos_events_processed.csv", "r")
log = dict()

def readFile():
    log[0] = []
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        parts = line.split(";")
        timestamp = parts[0]
        tempID = parts[1]
        component = parts[2]
        msg = parts[3]
        event = (timestamp, tempID, component, msg)
        log[0].append(event)
    file.close()


def sortLog():
    for caseId in sorted(log.keys()):
        log[caseId].sort(key=lambda event: event[-1])  # sort by timestamp
        for (task, user, timestamp) in log[caseId]:
            print(caseId, task, user, timestamp)