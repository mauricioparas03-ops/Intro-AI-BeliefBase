# AGM Operations
# Purpose: Modifies the Belief Base
# Components:
#   Expand: adds a formula to the set
#   Contract: uses inference engine to check for entailment, and removes formulas until the target is no logner entailed
#   Revise: combines the Expand and Contract (Levi identity? contract the negation, then expand)

from knowledge_representation import *
from inference_engine import entails, is_consistent

#Implement contraction (greedy version)
def contract(base: BeliefBase, formula: Formula) -> BeliefBase:
    new_base = base.copy()

    # Remove lowest priority formulas first
    for f in base.get_formulas():
        if entails(new_base, formula):
            # remove f
            new_base._beliefs = [(bf, p) for (bf, p) in new_base._beliefs if bf != f]

    return new_base

#Expansion
def expand(base, formula):
    new_base = base.copy()
    max_priority = max([p for _, p in base.get_with_priorities()], default=0)
    new_base.add(formula, priority=max_priority + 1)
    return new_base

#Revision (AGM identity)
def revise(base: BeliefBase, formula: Formula) -> BeliefBase:
    return expand(contract(base, Not(formula)), formula)

#First revision test
if __name__ == "__main__":
    p = Atom('p')
    q = Atom('q')

    B = BeliefBase()
    B.add(p, priority=1)
    B.add(p >> q, priority=2)

    print("Original:")
    print(B)

    print("\nRevise with ¬q:")
    B2 = revise(B, ~q)
    print(B2)

    #test
    print("Is revised base consistent?")
    print(is_consistent(B2)) #should be True

    #test
    p = Atom('p')
q = Atom('q')

B = BeliefBase()
B.add(p, priority=2)
B.add(p >> q, priority=1)

print("Original:")
print(B)

B2 = revise(B, ~q)

print("\nRevised:")
print(B2)