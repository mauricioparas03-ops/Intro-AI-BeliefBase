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

BELIEF BASE:
    A list of (formula, priority) pairs.
    Priority is a number you assign when adding a belief:
        higher number = more important = last to be removed
        lower number  = less important = first to be removed

The comments and documentation in this file were written with the help of AI
to make the reasoning and design decisions easier to follow for everyone in the group.
"""

# Base Class

class Formula(ABC):
    """
    Abstract base class for all propositional logic formulas.

    Every node in the AST inherits from this class.
    Defines operator overloads so formulas can be written naturally,
    and defines equality/hashing based on string representation.
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
    """
    the simplest formula.
    Examples: p, q, r, rain, sunny.
    Stores just a string name. Has no children.
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class Top(Formula):
    """
    Represents ⊤ (Tautology / always True).
    Used as a logical constant. Has no children.
    """
    def __repr__(self):
        return '⊤'


class Bot(Formula):
    """
    Represents ⊥ (Contradiction / always False).
    Used as a logical constant. Has no children.
    A belief base that entails ⊥ is inconsistent.
    """
    def __repr__(self):
        return '⊥'


# Compound Nodes

class Not(Formula):
    """
    Logical negation: ¬φ
    Has one child: the formula being negated.
    Example: Not(Atom('p')) represents ¬p
    """
    def __init__(self, formula: Formula):
        self.formula = formula

    def __repr__(self):
        return f'¬{repr(self.formula)}'


class And(Formula):
    """
    Logical conjunction: φ ∧ ψ
    Has two children: left and right.
    Example: And(Atom('p'), Atom('q')) represents (p ∧ q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} ∧ {repr(self.right)})'


class Or(Formula):
    """
    Logical disjunction: φ ∨ ψ
    Has two children: left and right.
    Example: Or(Atom('p'), Atom('q')) represents (p ∨ q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} ∨ {repr(self.right)})'


class Implies(Formula):
    """
    Logical implication: φ → ψ
    Has two children: left (antecedent) and right (consequent).
    Example: Implies(Atom('p'), Atom('q')) represents (p → q)
    During CNF conversion this gets eliminated: (p → q) becomes (¬p ∨ q)
    """
    def __init__(self, left: Formula, right: Formula):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'({repr(self.left)} → {repr(self.right)})'


class Biconditional(Formula):
    """
    Logical biconditional: φ ↔ ψ
    Has two children: left and right.
    Example: Biconditional(Atom('p'), Atom('q')) represents (p ↔ q)
    During CNF conversion this gets eliminated first:
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
    Convenience function for Biconditional.
    Python has no <=> operator so we cannot overload it.
    Use Bic(p, q) instead of Biconditional(p, q) for cleaner syntax.
    """
    return Biconditional(p, q)


# Step 5: BeliefBase

class BeliefBase:
    """
    The agent's belief base — a prioritised collection of propositional formulas.

    INTERNAL STRUCTURE:
        A list of (formula, priority) tuples.
        Priority is an integer: higher = more entrenched = removed last during contraction.

    Only the syntactic check is defined here.
    The semantic check is in inference_engine.py.
    """

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
        Syntactic membership check: is this exact formula stored in the base?
        Uses Formula.__eq__ which compares string representations.
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
        """Return raw (formula, priority) tuples sorted by priority ascending."""
        return sorted(self._beliefs, key=lambda x: x[1])

    def __le__(self, other: 'BeliefBase') -> bool:
        """
        Subset check: is every formula in self also in other?
        Used to test the Inclusion postulate: B * φ ⊆ B + φ
        """
        return all(f in other for f in self)

    def copy(self) -> 'BeliefBase':
        """
        Return an independent clone of this belief base.
        Mutating the copy does not affect the original.
        Essential for remainder set computation in revision_engine.py,
        where we trial-remove formulas without touching the real base.
        """
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



