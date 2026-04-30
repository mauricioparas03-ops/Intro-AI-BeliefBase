#test

from knowledge_representation import Atom, Bic, BeliefBase

p = Atom('p')
q = Atom('q')

# AST building
print(p & q)        # (p ∧ q)
print(p | q)        # (p ∨ q)
print(~p)           # ¬p
print(p >> q)       # (p → q)
print(Bic(p, q))    # (p ↔ q)

# Equality and hashing
print(Atom('p') == Atom('p'))   # True
print(Atom('p') == Atom('q'))   # False

# BeliefBase
B = BeliefBase()
B.add(p, priority=1)
B.add(p >> q, priority=2)
B.add(q, priority=3)

print(p in B)           # True
print(Atom('r') in B)   # False
print(B)

# Sorted by priority (lowest first = cut first)
print(B.get_formulas())

# Subset check
B2 = BeliefBase()
B2.add(p, priority=1)
print(B2 <= B)   # True
print(B <= B2)   # False

# Copy independence
B3 = B.copy()
B3.add(Atom('r'), priority=0)
print(Atom('r') in B)   # False — original untouched