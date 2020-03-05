#Title: Single thread Floyd-Warshall Algorithm
#Author: Daniel Pacheco
#Description: This script implements the Floyd-Warshall algorithm.

def readMatrixFromFile(filePath):
    file = open(filePath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
    return lines

def applySingleFloyd(graph):
    size = len(graph)
    for k in range(size):
        for i in range(size):
            for j in range(size):
                graph[i][j] = min(int(graph[i][j]), int(graph[i][k]) + int(graph[k][j]))
    return graph

if __name__ == "__main__":
    solvedGraph = readMatrixFromFile("fwTestResult.txt")
    testGraph = applySingleFloyd(readMatrixFromFile("fwTest.txt"))

    #compare results
    size = len(solvedGraph)
    for i in range(size):
        for j in range(size):
            sol = solvedGraph[i][j]
            tst = testGraph[i][j]
            print(f"{sol},{tst}")
    print("Completed!")
