# GaugeBlockCalculator / Endmaßrechner
Author: Anton CNC
YouTube: https://www.youtube.com/@boessi
This program has the following advantages:
-It is guaranteed to find the exact combination of end gauges if one exists.
-It uses recursion with backtracking to check all possible combinations.
-It takes floating point inaccuracies into account by using a very small tolerance value (1e-9).
-It outputs the combination found, the number of end gauges used, and the total sum.

To run the program, make sure you have Python and Tkinter installed.

The backtracking in this program works like this:
1.) The find_end_gauges function implements the backtracking algorithm. It tries to find a combination of end gauges
that exactly gives the target length.
2.) The algorithm starts with an empty combination and gradually adds end gauges.
3.) In each step, a end gauge is added to the current combination and checked:
-If the sum of the end gauges is equal to the target length, a solution has been found.
-If the sum is greater than the target length, this path is not useful.
-If the sum is smaller, the search continues recursively.
If a path does not lead to a solution, the algorithm "backtracks" by returning to the previous state and trying another option.

The process repeats until either a solution is found or all possibilities are exhausted.

Using a set (used_end_measurements) ensures that each end measure is used only once.

This approach makes it possible to search the solution space efficiently by terminating non-useful paths early.
