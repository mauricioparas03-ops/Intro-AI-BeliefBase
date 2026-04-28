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