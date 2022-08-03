import graph
import reader


def main():
    reader.readFile()
    print("\n\n")
    graph.getTransitionMatrix()
    #graph.printTransitionMatrix()

    graph.getActivityCount()
    #graph.printActivityCount()

    graph.generateGraph(graph.activityCount)


if __name__ == '__main__':
    main()
