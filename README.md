# Parallel-Floyd-Warshall

The Floyd-Warshall algorithm is an algorithm to find the shortest paths on a graph.
This script is able to read two matrices, a solved and an unsolved matrix (```fwTestResults.txt```
and ```fwTest.txt``` respectively), then it applies the algorithm on the unsolved matrix and compares the results with the solved matrix.

### Problems Encountered

While doing this assignment, I experienced several deadlock-causing scenarios. Debugging these was relatively straightforward using the ```comm.Get_rank()``` function from MPI. The work breakdown was significantly easier thanks to the equations.

### Existing Bugs

This script does not contain bugs I am aware of.

### How long to complete this assignment?

This assignment took me about a day, from start to finish.

### Performance measurements
*Single Thread:
*2 Threads:
*4 Threads:
*8 Threads:

### Behavior Analysis

### dumpCPUInfo.sh output




