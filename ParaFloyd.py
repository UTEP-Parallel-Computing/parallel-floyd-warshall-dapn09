#Title: Parallel Floyd-Warshall Algorithm
#Author: Daniel Pacheco
#Description: This script implements the Floyd-Warshall algorithm in parallel using MPI.

from mpi4py import MPI

def readMatrixFromFile(filePath):
    file = open(filePath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
    return lines

if __name__ == "__main__":
    refGraph = readMatrixFromFile("fwTestResult.txt")
    testGraph = readMatrixFromFile("fwTest.txt")

    size = len(testGraph)
    #Make matrix which will store the results.
    solvedGraph = [[0 for _ in range(size)] for __ in range(size)]

    #get world communicator
    comm = MPI.COMM_WORLD

    rowsPerThread = size//comm.Get_size()
    threadsPerRow = comm.Get_size()/size
    startRow = rowsPerThread*comm.Get_rank()
    endRow = rowsPerThread*(comm.Get_rank() + 1)

    for k in range(size):
        ownerOfRow = int(threadsPerRow*k)
        testGraph[k] = comm.bcast(testGraph[k], root=int(threadsPerRow*k))
        for i in range(startRow, endRow):
            for j in range(size):
                if i != j:
                    testGraph[i][j] = min(int(testGraph[i][j]), int(testGraph[i][k]) + int(testGraph[k][j]))


    if comm.Get_rank() == 0:
        for k in range(endRow, size):
            ownerOfK = int((comm.Get_size()/size)*k)
            testGraph[k] = comm.recv(source=ownerOfK, tag=42)

        #compare results
        for i in range(size):
            for j in range(size):
                sol = int(refGraph[i][j])
                tst = int(testGraph[i][j])
                if sol != tst:
                    print(f"Discrepancies found in row:{i}, col:{j}")
    elseo
        for k in range(startRow, endRow):
            comm.send(testGraph[k], dest=0, tag=42)
