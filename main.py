import pygraphviz as pgv
import graph
import reader

print("main   mmm")
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


def main():
    reader.readFile()
    reader.sortLog()
    for caseId in reader.log:
        print("id ", caseId)
        for (task, user, timestamp) in reader.log[caseId]:
            print(task, user, timestamp)

    graph.getTransitionMatrix()
    graph.printTransitionMatrix()

    graph.getActivityCount()
    graph.printActivityCount()

    graph.generateGraph(graph.activityCount)


if __name__ == '__main__':
    main()
