#Title: Parallel Floyd-Warshall Algorithm
#Author: Daniel Pacheco
#Description: This script implements the Floyd-Warshall algorithm in parallel using MPI.

from mpi4py import MPI
import matrixUtils as mu

def readMatrixFromFile(filePath):
    file = open(filePath, 'r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split()
    return lines

if __name__ == "__main__":

    #get world communicator
    comm = MPI.COMM_WORLD

    #Read the file containing the test matrix.
    testGraph = readMatrixFromFile("fwTest.txt")
    #Read the file with the correct answers.
    refGraph = readMatrixFromFile("fwTestResult.txt")

    if comm.Get_rank() == 0:

        print("\nInput matrices:\n\n")
        print("Test Matrix:")
        mu.printSubarray(testGraph, size=6)
        #New line
        print()

        print("\nTarget Matrix:")
        mu.printSubarray(refGraph, size=6)
        #New line
        print()

    #Useful formulas
    size = len(testGraph)
    rowsPerThread = size//comm.Get_size()
    threadsPerRow = comm.Get_size()/size
    startRow = rowsPerThread*comm.Get_rank()
    endRow = rowsPerThread*(comm.Get_rank() + 1)

    #Parallel Floyd-Warshall algorithm
    for k in range(size):
        ownerOfRow = int(threadsPerRow*k)
        testGraph[k] = comm.bcast(testGraph[k], root=int(threadsPerRow*k))
        for i in range(startRow, endRow):
            for j in range(size):
                if i != j:
                    testGraph[i][j] = min(int(testGraph[i][j]), int(testGraph[i][k]) + int(testGraph[k][j]))

    #Assemble results
    if comm.Get_rank() == 0:
        for k in range(endRow, size):
            ownerOfK = int((comm.Get_size()/size)*k)
            testGraph[k] = comm.recv(source=ownerOfK, tag=42)

        print("Output matrices:\n\n")
        print("Test Matrix:")
        mu.printSubarray(testGraph, size=6)
        print()
        print("\nTarget Matrix:")
        mu.printSubarray(refGraph, size=6)
        print()

        #Compare results
        discrepFound = False
        for i in range(size):
            for j in range(size):
                sol = int(refGraph[i][j])
                tst = int(testGraph[i][j])
                if sol != tst:
                    discrepFound = True
        if discrepFound:
            print(f"Discrepancies found!!!")
        else:
            print("Both matrices match!!!")
    else:
        for k in range(startRow, endRow):
            comm.send(testGraph[k], dest=0, tag=42)
