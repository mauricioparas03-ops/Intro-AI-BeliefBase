# Entailment Checker
# Purpose: determines if a formula is logically entailed by the current belif base w/o external packages
# Components: a conjunctive normal form (CNF) converter to normalize formulas
#   a resolution alg that attempts to derive an empty clause from the negation of the query

from knowledge_representation import *

#Eliminate implications & biconditionals
#We first simplify formulas so only ¬, ∧, ∨ remain.

def eliminate_implications(formula: Formula) -> Formula:
    if isinstance(formula, Atom) or isinstance(formula, Top) or isinstance(formula, Bot):
        return formula

    if isinstance(formula, Not):
        return Not(eliminate_implications(formula.formula))

    if isinstance(formula, And):
        return And(
            eliminate_implications(formula.left),
            eliminate_implications(formula.right)
        )

    if isinstance(formula, Or):
        return Or(
            eliminate_implications(formula.left),
            eliminate_implications(formula.right)
        )

    if isinstance(formula, Implies):
        # p → q ≡ ¬p ∨ q
        return Or(
            Not(eliminate_implications(formula.left)),
            eliminate_implications(formula.right)
        )

    if isinstance(formula, Biconditional):
        # p ↔ q ≡ (p → q) ∧ (q → p)
        left = eliminate_implications(Implies(formula.left, formula.right))
        right = eliminate_implications(Implies(formula.right, formula.left))
        return And(left, right)

    raise ValueError("Unknown formula type")

#Push negations inward (NNF): now we move ¬ all the way to atoms.
def move_not_inwards(formula: Formula) -> Formula:
    if isinstance(formula, Atom):
        return formula

    if isinstance(formula, Not):
        inner = formula.formula

        # Double negation
        if isinstance(inner, Not):
            return move_not_inwards(inner.formula)

        # De Morgan rules
        if isinstance(inner, And):
            return Or(
                move_not_inwards(Not(inner.left)),
                move_not_inwards(Not(inner.right))
            )

        if isinstance(inner, Or):
            return And(
                move_not_inwards(Not(inner.left)),
                move_not_inwards(Not(inner.right))
            )

        return Not(move_not_inwards(inner))

    if isinstance(formula, And):
        return And(
            move_not_inwards(formula.left),
            move_not_inwards(formula.right)
        )

    if isinstance(formula, Or):
        return Or(
            move_not_inwards(formula.left),
            move_not_inwards(formula.right)
        )

    return formula

#Distribute OR over AND (CNF)
def distribute_or_over_and(formula: Formula) -> Formula:
    if isinstance(formula, And):
        return And(
            distribute_or_over_and(formula.left),
            distribute_or_over_and(formula.right)
        )

    if isinstance(formula, Or):
        left = distribute_or_over_and(formula.left)
        right = distribute_or_over_and(formula.right)

        # (A ∨ (B ∧ C)) → (A ∨ B) ∧ (A ∨ C)
        if isinstance(right, And):
            return And(
                distribute_or_over_and(Or(left, right.left)),
                distribute_or_over_and(Or(left, right.right))
            )

        # ((A ∧ B) ∨ C) → (A ∨ C) ∧ (B ∨ C)
        if isinstance(left, And):
            return And(
                distribute_or_over_and(Or(left.left, right)),
                distribute_or_over_and(Or(left.right, right))
            )

        return Or(left, right)

    return formula

#Full CNF pipeline
def to_cnf(formula: Formula) -> Formula:
    step1 = eliminate_implications(formula)
    step2 = move_not_inwards(step1)
    step3 = distribute_or_over_and(step2)
    return step3

#Extract clauses
def extract_clauses(formula: Formula):
    clauses = []

    def extract_clause(f):
        if isinstance(f, Or):
            return extract_clause(f.left) | extract_clause(f.right)
        elif isinstance(f, Not):
            return {f"~{f.formula}"}
        elif isinstance(f, Atom):
            return {f"{f}"}
        else:
            raise ValueError("Unexpected formula in clause")

    def recurse(f):
        if isinstance(f, And):
            recurse(f.left)
            recurse(f.right)
        else:
            clauses.append(extract_clause(f))

    recurse(formula)
    return clauses

#Resolution rule
def resolve(c1, c2):
    resolvents = []

    for literal in c1:
        if literal.startswith("~"):
            complement = literal[1:]
        else:
            complement = "~" + literal

        if complement in c2:
            new_clause = (c1 - {literal}) | (c2 - {complement})
            resolvents.append(new_clause)

    return resolvents

#Entailment
def entails(base: BeliefBase, query: Formula) -> bool:
    clauses = []

    # Add base clauses
    for f in base:
        cnf = to_cnf(f)
        clauses.extend(extract_clauses(cnf))

    # Add negated query
    neg_query = Not(query)
    cnf_neg = to_cnf(neg_query)
    clauses.extend(extract_clauses(cnf_neg))

    clauses = [frozenset(c) for c in clauses]
    clauses_set = set(clauses)

    while True:
        new = set()

        clause_list = list(clauses_set)

        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                resolvents = resolve(clause_list[i], clause_list[j])

                for r in resolvents:
                    if not r:
                        return True  # empty clause found

                    new.add(frozenset(r))

        if new.issubset(clauses_set):
            return False

        clauses_set |= new

#Consistency check
def is_consistent(base: BeliefBase) -> bool:
    return not entails(base, Bot())

#Test 0
if __name__ == "__main__":
    p = Atom('p')
    q = Atom('q')

    B = BeliefBase()
    B.add(p)
    B.add(p >> q)

    print("Beliefs:")
    print(B)

    print("Does B entail q?")
    print(entails(B, q))  # should be True

# #Test 1 — Non-entailment
# p = Atom('p')
# q = Atom('q')

# B = BeliefBase()
# B.add(p)

# print(entails(B, q))  # should be False

# #Test 2 — Simple contradiction
# p = Atom('p')

# B = BeliefBase()
# B.add(p)
# B.add(~p)

# print(is_consistent(B))  # should be False

# #Test 3 — Chain reasoning
# p = Atom('p')
# q = Atom('q')
# r = Atom('r')

# B = BeliefBase()
# B.add(p)
# B.add(p >> q)
# B.add(q >> r)

# print(entails(B, r))  # should be True

# #Test 4 — OR reasoning
# p = Atom('p')
# q = Atom('q')

# B = BeliefBase()
# B.add(p | q)
# B.add(~p)

# print(entails(B, q))  # should be True

# #Test 5 — No explosion unless contradiction
# p = Atom('p')
# q = Atom('q')

# B = BeliefBase()
# B.add(p | q)

# print(entails(B, p))  # should be False