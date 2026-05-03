# Belief Revision Assignment
**02180 Introduction to Artificial Intelligence**
**Group 27**

## Overview
This project implements a custom Belief Revision Engine that operates on propositional logic in its symbolic form. The agent maintains a belief base with priority order. When new, contradictory information is introduced, the engine uses partial meet contraction and AGM revision principles to update the agent's beliefs while keeping logical consistency.

## Project Architecture
The project is divided into the following Python files:

* **`knowledge_representation.py`**: The data layer. Defines the Abstract Syntax Tree (AST) for logical formulas (Atoms, And, Or, Not, Implies, Biconditional) and manages the `BeliefBase` object, which stores formulas with their priority weights.
* **`inference_engine.py`**: The logic processor. Converts formulas to Conjunctive Normal Form (CNF) and performs resolution based logical entailment checks.
* **`revision_engine.py`**: The controller. Implements the AGM operations: Expansion, Partial Meet Contraction (using remainder sets and priority scoring), and Revision via the Levi identity.
* **`test_suite.py`**: The validator. A test suite that tests the engine by verifying compliance with the AGM postulates.
* **`run_example.py`**: An example script using week 10 exercises, that show logical entailment and partial meet contraction.

## Prerequisites
This project requires **Python 3.8+**. 

Because the inference engine was built from scratch, **no external Python packages or virtual environments are required** to run the core logic or the test suite.

---

## 1. Jupyter Notebook Demo - Recommended
We have included an interactive Jupyter Notebook (`demo.ipynb`) to easily test the system. You can open and run this notebook to step through the logical entailment and partial meet contraction examples.

---

## 2. Automated Postulate Testing
To verify the engine with the AGM postulates, please run the automated test suite from the root directory:
```bash
python test_suite.py
