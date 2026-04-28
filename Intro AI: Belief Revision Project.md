Intro AI: Belief Revision Project

Task implement a belief revision agent

1. design and implementation of belief base;

    - Database of beliefs (dictionary)

2. design and implementation of a method for checking logical entailment (e.g., resolutionbased), you should implement it yourself, without using any existing packages;

    - Logical Entailment (The "read" engine)
    aka the truth checker. does not modify or change the belief base at all only evaluates it

        # What it does:
        - Takes the current belief base ($B$) and a target formula ($\phi$), and answers a strict Yes/No question: Based on what the agent currently believes, is this formula logically true? ($B \models \phi$)

        # How it works:
        - If the belief base contains p and p -> q, and q is quieried, the entailment engine runs an algorithm (like resolution) to prove that q is an unavoidable conclusion

        # Challenge:
        - Cannot use existing Python packages for this. Have to code the algorithm that converts formulas to Conjunctive Normal Form (CNF) and resolves the clauses manually.


3. implementation of contraction of belief base (based on a priority order on formulas in the
belief base);
4. implementation of expansion of belief base
The output should be the resulting/new belief base.

(*) If you prefer, you can choose to implement belief revision on plausibility orders. Your project should then run through the following sequence of stages:

1. design and implementation of a plausibility order on possible worlds;

2. design and implementation a method for checking logical entailment (whether or not the formula is true in all of the minimal/best states);

3. design and implementation a revision method (lexicographic or minimal) of the plausibility
order.
The output should be the resulting/new plausibility order.


### Abstract Syntax Tree (AST) & Logical Symbology

The following tables define the formal mathematical symbols used to represent our propositional logic framework, alongside their corresponding programmatic implementations in the AST.

#### 1. Logical Connectives (AST Nodes)

These symbols represent the core nodes within our Abstract Syntax Tree used to build propositional formulas.

| Concept | Mathematical Symbol | Python Operator Override | AST Node Class | Syntax Example |
| :--- | :---: | :---: | :--- | :--- |
| **NOT** | $\neg$ | `~` | `Not` | `~p` |
| **AND** | $\land$ | `&` | `And` | `p & q` |
| **OR** | $\lor$ | `|` | `Or` | `p | q` |
| **Implication** | $\implies$ | `>>` | `Implies` | `p >> q` |
| **Biconditional**| $\iff$ | `<=>` | `Biconditional`| `p <=> q` |
| **True (Tautology)** | $\top$ | `True` | `Top` | $\top$ |
| **False (Contradiction)** | $\bot$ | `False` | `Bot` | $\bot$ |

#### 2. Set Theory & Belief Operations

These symbols are used in the documentation and test suite to define the rules of the Belief Base ($B$), the inference engine, and the AGM postulates.

| Concept | Mathematical Symbol | Project Usage | Python Method | Syntax Example |
| :--- | :---: | :--- | :--- | :--- |

| **Element of** | $\in$ | $\phi \in B$ (Formula is a current belief) | __contains__(self, item) | `p in B` |
| **Subset of** | $\subseteq$ | $B' \subseteq B$ (Comparing belief base states) | __le__(self, other) | `B1' <= B2` |
| **Equivalence** | $\equiv$ | $\phi \equiv \psi$ (Logical equivalence for the Extensionality postulate) | __eq__(self, other) | `p == q` |
| **Entailment** | $\models$ | $B \models \phi$ (The inference engine proves the formula) | ? | ? |
| **Expansion** | $+$ | $B + \phi$ (Blindly adding a belief) | __add__(self, other) | `B + p` |
| **Contraction** | $-$ | $B - \phi$ (Removing a belief and resolving dependencies) | __sub__(self, other) | `B - p` |
| **Revision** | $*$ | $B * \phi$ (Adding a belief while maintaining consistency) | __mul__(self, other) | `B * p` |





