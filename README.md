# CS440-Intro-AI-Project-3

SUMMARY:

The purpose of this assignment is to model your knowledge/belief about a system probabilistically, and use this belief state to efficiently direct future action.


If you find the target, you are done. The goal is to locate the target in as few searches as possible by utilizing the results of the observations collected.

Implementation: Maps may be generated in the following way: for a 50 by 50 grid, randomly assign each cell a terrain type, (flat with probability 0.25, hilly with probability 0.25, forested with probability 0.25, and caves with probability 0.25). Select a cell uniformly at random, and set this as the location of the target. Note, this information represents the environment. The location of the target is hidden from your agent, but the agent knows each cell type and can query the environment about a requested cell.

At any time t, given the current state of Belief, the agent must determine a cell to check by some rule and search it. If the cell does not contain the target, the environment will return failure. If the environment does contain the target, the search will return failure or success with the appropriate probabilities, based on the terrain type. If the search returns failure, for whatever reason, use this observation about the selected cell to update your belief state for all cells (using Bayes’ Theorem). If the search returns success, return the total number of searches taken to locate the target.

MORE INFO: Assignment3.pdf

FINAL REPORT: AI_3.pdf
