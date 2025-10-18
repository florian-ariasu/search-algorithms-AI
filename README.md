# AI Search Algorithms

This project focuses on implementing and comparing various AI search algorithms. The algorithms were tested using **Sokoban** as the problem domain (Sokoban itself was not implemented by me, only used as a test environment).

---

## Before Proceeding

> [!IMPORTANT]
> This is a homework project for AI class (3rd year, 2nd sem)
- This was implemented with the use of LLMs, copilot agent and Chat GPT
- Please, use with caution because it may have unexpected bugs or unwanted behaviours
- Educational purposes only

---

## Algorithms Implemented

For this project I have implemented and tested the following AI search algorithms:

- **IDA*** – Iterative Deepening A*  
- **Push_IDA*** – attempted (not fully functional)  
- **A*** – basic version (h(n) = 0, equivalent to Dijkstra)  
- **A* with Manhattan distance heuristic**  
- **A* with Manhattan + Deadlock Detection**  
- **Push_A*** – attempted (not fully functional)  
- **Simulated Annealing (Simanneal)**  

---

## Feature Description

**Note:** This project's main contribution is the implementation of the AI search algorithms listed above. Sokoban is used solely as a benchmark problem to test and compare the algorithms' performance. The Sokoban game logic itself was not implemented by me.

### Development Process
- Started with **IDA***, which works on smaller test cases (`easy_map1`, `easy_map2`, `medium_map1`) but becomes inefficient for larger maps.  
- Implemented **A***, which performs much better, especially with heuristics.  
- Added **Manhattan distance heuristic** to improve efficiency and reduce explored states.  
- Extended A* with a **Deadlock Detection strategy** (blocking boxes in corners), further reducing unnecessary exploration.  
- Attempted **Push-based algorithms (Push_IDA*, Push_A*)** to reduce search space, but they are not functional due to insufficient heuristics, incomplete pruning, and deadlock checks.  
- Implemented **Simulated Annealing**, which always finds a solution but explores a very large search space and is stochastic (different execution times per run).  

### Algorithm Comparisons
- **IDA*** is complete but inefficient for large maps, repeating many identical searches.  
- **A*** is deterministic, generally optimal in explored states, but sensitive to heuristic quality. On extreme cases (like `super_hard_map1`), it may “explode” in state space.  
- **Simulated Annealing** guarantees a solution and avoids local minima but is non-optimal and stochastic.  

### Observations
- On **medium maps**, A* significantly outperforms IDA*.  
- On **large maps**, A* remains more efficient, though Simanneal may solve instances where A* consumes too much memory.  
- On **super hard maps**, A* can fail without a strong heuristic, while Simanneal succeeds at the cost of more moves.  

### Metrics & Graphs
- Compared algorithms based on:
  - Success rate  
  - Number of pulls  
  - Execution time  
  - Total number of moves  
- Graphs (bar plots, tables) were generated with **Matplotlib**, **Pandas**, and **Seaborn**.  

### OOP & Design Choices
- The AI search algorithms are implemented in the **`/src`** directory (e.g., `a_star.py`, `ida_star.py`, `simulated_annealing.py`, etc.).  
- **`main.py`** is the entry point of the program, orchestrating the search algorithms on Sokoban test maps.  
- **`main.ipynb`** was used for visualising algorithm performance with graphs.  

---

## Running the Project

There are two main ways to run the program:

1. **Using `main.py`:**
   ```bash
   python3 main.py tests/large_map2.yaml
   python3 main.py 'simanneal' tests/hard_map1.yaml
   python3 main.py   # runs default test from main.py
   ```

2. **Using Jupyter Notebook (`main.ipynb`):**
   - Run all cells to generate performance graphs and tables.  

Output is displayed in the terminal in structured form after each run.  

---

## Tools & Libraries
- **Python 3**  
- **Matplotlib**, **Pandas**, **Seaborn** (for metrics & graphs)  

---

## Conclusion
- **IDA***: Complete, works fine on small/medium tests, but inefficient for large maps.  
- **A***: Most optimal in terms of explored states, deterministic, but can fail on extreme cases without strong heuristics.  
- **Simulated Annealing**: Always guarantees a solution, avoids local minima, fastest in runtime, but not optimal.  

---

## Bonus / Future Improvements
- **Push-based algorithms (Push_A*, Push_IDA*)** could be improved by:  
  - Enhancing **deadlock detection** (not just simple corner blocking).  
  - Using a more **informative heuristic** than Manhattan distance.  
  - Implementing stronger **pruning strategies** to reduce redundant searches.  
  - Fixing existing **bugs** in state management and move validation.  
- Explore hybrid approaches combining deterministic search (A*) with stochastic search (Simanneal).  
- Implement parallel execution for Simanneal to reduce runtime variability.

## Licence
This project is licensed under the MIT Licence. See the [LICENSE](./LICENSE) file for further details.  
