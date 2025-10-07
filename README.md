# Sokoban HW AI

## Algorithms Implemented

For this project I have implemented and tested the following algorithms:

- **IDA*** – Iterative Deepening A*  
- **Push_IDA*** – attempted (not fully functional)  
- **A*** – basic version (h(n) = 0, equivalent to Dijkstra)  
- **A* with Manhattan distance heuristic**  
- **A* with Manhattan + Deadlock Detection**  
- **Push_A*** – attempted (not fully functional)  
- **Simulated Annealing (Simanneal)**  

---

## Feature Description

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
- Algorithms are implemented in the **`/search_methods`** directory.  
- **`main.py`** is the entry point of the program.  
- **`main.ipynb`** was used for visualising performance with graphs.  

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
- Explore hybrid approaches combining deterministic search (A*) with stochastic search (Simanneal).  
- Implement parallel execution for Simanneal to reduce runtime variability.  

---

## Licence
This project is licensed under the MIT Licence. See the [LICENSE](./LICENSE) file for further details.  
