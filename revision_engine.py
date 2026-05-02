# AGM Operations
# Purpose: Modifies the Belief Base
# Components:
#   Expand: adds a formula to the set
#   Contract: uses inference engine to check for entailment, and removes formulas until the target is no logner entailed
#   Revise: combines the Expand and Contract (Levi identity? contract the negation, then expand)

from knowledge_representation import *
from inference_engine import entails, is_consistent

#Implement contraction (grredy))
#def contract(base: BeliefBase, formula: Formula) -> BeliefBase:
#    from inference_engine import to_cnf
#
#    new_base = base.copy()
#    target = to_cnf(formula)
#
#    for f in base.get_formulas():
#        if entails(new_base, target):
#           new_base._beliefs = [(bf, p) for (bf, p) in new_base._beliefs if bf != f]
#
#    return new_base

#partial meet contraction
import itertools
def all_subsets(formulas):
    """
    Generate all subsets of a list of formulas.
    WARNING: exponential, but fine for small belief bases.
    """
    subsets = []
    for r in range(len(formulas) + 1):
        subsets.extend(itertools.combinations(formulas, r))
    return subsets

def remainder_sets(base: BeliefBase, formula: Formula):
    """
    Compute all remainder sets:
    maximal subsets of base that do NOT entail formula.
    """
    candidates = []
    formulas = base.get_formulas()

    # 1. generate all subsets
    for subset in all_subsets(formulas):
        temp = BeliefBase()

        # rebuild belief base from subset
        for f in subset:
            # keep original priorities
            for bf, p in base.get_with_priorities():
                if bf == f:
                    temp.add(bf, p)

        # 2. check if subset does NOT entail formula
        if not entails(temp, formula):
            candidates.append(temp)

    # 3. keep only MAXIMAL subsets
    maximal = []
    for c in candidates:
        is_maximal = True
        for other in candidates:
            if c != other and set(c.get_formulas()) < set(other.get_formulas()):
                is_maximal = False
                break
        if is_maximal:
            maximal.append(c)

    return maximal

def score(base: BeliefBase, original: BeliefBase):
    """
    Score = sum of priorities of formulas preserved from original base.
    Higher score = better remainder set.
    """
    total = 0
    for f, p in original.get_with_priorities():
        if f in base:
            total += p
    return total

def select(remainders, original):
    """
    Select best remainder sets (highest priority retention).
    """
    if not remainders:
        return []

    best_score = max(score(r, original) for r in remainders)
    return [r for r in remainders if score(r, original) == best_score]

#Intersection of selected sets
def intersect_bases(bases):
    """
    Intersect multiple belief bases (keep only common formulas).
    """
    if not bases:
        return BeliefBase()

    common = set(bases[0].get_formulas())

    for b in bases[1:]:
        common &= set(b.get_formulas())

    result = BeliefBase()

    # restore priorities from original bases (approximation)
    for f in common:
        result.add(f)

    return result

def contract(base: BeliefBase, formula: Formula) -> BeliefBase:
    """
    AGM Partial Meet Contraction
    """
    from inference_engine import to_cnf

    # normalize formula
    target = to_cnf(formula)

    # 1. compute remainder sets
    remainders = remainder_sets(base, target)

    if not remainders:
        return BeliefBase()

    # 2. select best ones (priority-based)
    selected = select(remainders, base)

    # 3. intersect them
    result = intersect_bases(selected)

    return result

#Expansion
from inference_engine import to_cnf

def expand(base, formula):
    new_base = base.copy()

    # Normalize formula before adding
    normalized = to_cnf(formula)

    max_priority = max([p for _, p in base.get_with_priorities()], default=0)
    new_base.add(normalized, priority=max_priority + 1)

    return new_base

#Revision (AGM identity)
def revise(base: BeliefBase, formula: Formula) -> BeliefBase:
    return expand(contract(base, Not(formula)), formula)

    
   