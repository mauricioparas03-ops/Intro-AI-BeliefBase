# Core Data
# Purpose: defines the Abstract Syntax Tre (AST) for logical formulas
# Components: Classes for Var, Not, And, Or, and Implies
# Belief Base: a belief base class that stores a set of these formula objects and maintains the priority ordering used for contraction

# knowledge_representation.py

from abc import ABC, abstractmethod

"""
knowledge_representation.py
============================

This defines how formulas are built and stored.

SYMBOLS AND WHAT THEY MEAN:
    Math    Code        Meaning
    ────────────────────────────────────────────────────────
    ⊤       Top()       always true
    ⊥       Bot()       always false
    ¬p      ~p          flips true to false and vice versa
    ∧       p & q       true only if both sides are true
    ∨       p | q       true if at least one side is true
    →       p >> q      false only if left is true and right is false
    ↔       Bic(p, q)   true only if both sides have the same value

EQUALITY:
    Two formulas are equal if they look the same as text.
    And(p, q) == And(p, q) is True.

"""

# Base Class

class Formula(ABC):
    """
    Abstract base class for all propositional logic formulas.
    """

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)

    def __rshift__(self, other):
        return Implies(self, other)

    def __eq__(self, other):
        return isinstance(other, Formula) and repr(self) == repr(other)

    def __hash__(self):
        return hash(repr(self))

    @abstractmethod
    def __repr__(self):
        pass


# Leaf Nodes

class Atom(Formula):

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class Top(Formula):
    """
    Represents ⊤ (Tautology / always True).
    """
    def __repr__(self):
        return '⊤'


class Bot(Formula):
    """
    Represents ⊥ (Contradiction / always False).
    """
    def __repr__(self):
        return '⊥'


# Compound Nodes

class Not(Formula):
    """
    Logical negation 
    """
    def __init__(self, formula: Formula):
        self.formula = formula

    def __repr__(self):
        return f'¬{repr(self.formula)}'


class And(Formula):
    """
    (p ∧ q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} ∧ {repr(self.right)})'


class Or(Formula):
    """
     (p ∨ q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} ∨ {repr(self.right)})'


class Implies(Formula):
    """
    (p → q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} → {repr(self.right)})'


class Biconditional(Formula):
    """
        (p ↔ q) becomes ((p → q) ∧ (q → p))
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} ↔ {repr(self.right)})'


# Step 4: Biconditional helper

def Bic(p: Formula, q: Formula) -> Biconditional:
    """
    Used to create a biconditional formula from two formulas p and q.
    """
    return Biconditional(p, q)


# Step 5: BeliefBase

class BeliefBase:

    def __init__(self):
        self._beliefs: list[tuple[Formula, int]] = []

    def add(self, formula: Formula, priority: int = 0):
        """
        Add a formula with a priority.
        If the formula already exists, update its priority instead of duplicating.
        """
        for i, (f, _) in enumerate(self._beliefs):
            if f == formula:
                self._beliefs[i] = (formula, priority)
                return
        self._beliefs.append((formula, priority))

    def __contains__(self, formula: Formula) -> bool:
        """
        is this exact formula stored in the base?
        Uses Formula.__eq__ which compares strings
        """
        return any(f == formula for f, _ in self._beliefs)

    def __iter__(self):
        """Iterate over just the formulas (not priorities)."""
        for f, _ in self._beliefs:
            yield f

    def get_formulas(self) -> list[Formula]:
        """
        Return formulas sorted by priority ascending.
        Lowest priority first = these are cut first during contraction.
        """
        return [f for f, _ in sorted(self._beliefs, key=lambda x: x[1])]

    def get_with_priorities(self) -> list[tuple[Formula, int]]:
        """Return raw (formula, priority) tuples sorted by priority ascending.
        Might not be used but it is nice to have for debugging."""
        return sorted(self._beliefs, key=lambda x: x[1])

    def __le__(self, other: 'BeliefBase') -> bool:
        """
        Is every formula in self also in other?
        """
        return all(f in other for f in self)

    def copy(self) -> 'BeliefBase':
        
        new_base = BeliefBase()
        new_base._beliefs = self._beliefs.copy()
        return new_base

    def __repr__(self) -> str:
        if not self._beliefs:
            return 'BeliefBase(∅)'
        lines = ['BeliefBase:']
        for f, p in sorted(self._beliefs, key=lambda x: x[1]):
            lines.append(f'  priority={p} | {repr(f)}')
        return '\n'.join(lines)



