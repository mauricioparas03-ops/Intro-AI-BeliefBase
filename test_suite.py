# Validator
# Purpose: Proves the engine works
# Tests AGM postulates (Closure, Success, Inclusion, Vacuity, Consistency, Extensionality, Superexpansion, Subexpansion) against operations in revision_engine.py

# AGM Rationality Postulates of Contraction (Lecture 11 slide 5)
# Closure
# Success
# Inclusion
# Vacuity
# Consistency
# Extensionality
# Conjunctive inclusion
# Conjunctive overlap


# AGM Rationality Postulates of Contraction (Lecture 11 slide 6)
# Closure
# Success
# Inclusion
# Vacuity
# Consistency
# Extensionality
# Superexpansion
# Subexpansion

from knowledge_representation import *
from inference_engine import entails, is_consistent
from revision_engine import revise, expand

#Success Postulate: after revision, the new belief must be included.
def test_success():
    p = Atom('p')
    q = Atom('q')

    B = BeliefBase()
    B.add(p)

    B2 = revise(B, q)

    print("Success:", q in B2) #expected true

#Inclusion Postulate: Revised base is a subset of expanded base
def test_inclusion():
    p = Atom('p')
    q = Atom('q')

    B = BeliefBase()
    B.add(p)

    rev = revise(B, q)
    exp = expand(B, q)

    print("Inclusion:", rev <= exp) #expected true

#Vacuity Postulate: If the belief is already in the base, revision should not change it.
def test_vacuity():
    p = Atom('p')
    q = Atom('q')

    B = BeliefBase()
    B.add(p)

    # B does NOT entail ¬q
    rev = revise(B, q)
    exp = expand(B, q)

    same = set(rev.get_formulas()) == set(exp.get_formulas())
    print("Vacuity:", same) #expected true

#Consistency Postulate: If the new belief is consistent, the revised base should also be consistent.
def test_consistency():
    p = Atom('p')

    B = BeliefBase()
    B.add(p)

    B2 = revise(B, ~p)

    print("Consistency:", is_consistent(B2)) #expected true

#Extensionality Postulate: If two beliefs are logically equivalent, revising by either should yield the same result.
def test_extensionality():
    p = Atom('p')
    q = Atom('q')

    phi = p >> q
    psi = (~p | q)  # equivalent to p → q

    B = BeliefBase()
    B.add(p)

    B1 = revise(B, phi)
    B2 = revise(B, psi)

    same = set(B1.get_formulas()) == set(B2.get_formulas())
    print("Extensionality:", same) #expected true

#run tests
if __name__ == "__main__":
    test_success()
    test_inclusion()
    test_vacuity()
    test_consistency()
    test_extensionality()