# Core Data
# Purpose: defines the Abstract Syntax Tre (AST) for logical formulas
# Components: Classes for Var, Not, And, Or, and Implies
# Belief Base: a belief base class that stores a set of these formula objects and maintains the priority ordering used for contraction

# knowledge_representation.py

from abc import ABC, abstractmethod

"""
knowledge_representation.py
============================

PURPOSE:
    This file is the data layer of the belief revision engine.
    It defines how propositional logic formulas are represented in memory
    (as Abstract Syntax Trees), and how a collection of beliefs is stored
    (as a BeliefBase). Nothing intelligent happens here — no reasoning,
    no entailment, no revision. It is purely structure.

WHAT IS AN AST?
    An Abstract Syntax Tree is a tree structure where:
    - Leaf nodes are the simplest building blocks: Atoms (p, q, r...), Top (⊤), Bot (⊥)
    - Compound nodes combine formulas using logical connectives: Not, And, Or, Implies, Biconditional
    - Example: "p → q" becomes Implies(Atom('p'), Atom('q'))
    - Example: "p ∧ ¬q" becomes And(Atom('p'), Not(Atom('q')))

    The tree structure means every formula can be recursively decomposed,
    which is essential for CNF conversion and resolution in inference_engine.py.

OPERATOR OVERLOADING:
    Python allows us to redefine what symbols like &, |, ~, >> do for our classes.
    We use this so formulas can be written naturally:
        p & q       instead of     And(p, q)
        p | q       instead of     Or(p, q)
        ~p          instead of     Not(p)
        p >> q      instead of     Implies(p, q)
    Python has no <=> operator, so Biconditional uses a helper function Bic(p, q).

EQUALITY AND HASHING:
    Two formulas are equal if their string representations are equal.
    This means And(Atom('p'), Atom('q')) == And(Atom('p'), Atom('q')) is True.
    Hashing is also based on repr() so formulas can be stored in Python sets and dicts.
    This is important for:
        - Checking if a formula is in the BeliefBase (syntactic membership)
        - Computing remainder sets in revision_engine.py (which uses set operations)

BELIEF BASE:
    The BeliefBase stores (formula, priority) pairs in a list.
    Priority is an integer assigned when a formula is added:
        - Higher priority = more entrenched = harder to remove during contraction
        - Lower priority = less important = removed first during contraction
    This ordering is what makes our contraction a *partial meet* contraction —
    we use priority to select which remainder sets to keep.

    Key distinction:
        - "p in B" is a SYNTACTIC check — is this exact formula stored?
        - "B.entails(p)" is a SEMANTIC check — does B logically imply p?
          That second operation is NOT defined here. It lives in inference_engine.py.

FILE DEPENDENCIES:
    - This file imports nothing from our project.
    - inference_engine.py imports Formula, Atom, Not, And, Or, Implies, Biconditional, BeliefBase
    - revision_engine.py imports BeliefBase and formula classes
    - test_suite.py imports everything

CHECKLIST (what should work after this file):
    [ ] Atom('p') creates a leaf node with name 'p'
    [ ] p & q, p | q, ~p, p >> q, Bic(p,q) all build correct AST nodes
    [ ] repr() of each node prints a readable formula
    [ ] Two Atom('p') instances are equal and hash the same
    [ ] BeliefBase.add() does not duplicate formulas, updates priority instead
    [ ] copy() produces an independent clone — mutating one does not affect the other
    [ ] get_formulas() returns formulas sorted by priority ascending (lowest first)
    [ ] __le__ correctly checks if one BeliefBase is a subset of another
"""

# Step 1: Base Class

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


# Step 2: Leaf Nodes

class Atom(Formula):
    """
    A propositional variable — the simplest formula.
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


# Step 3: Compound Nodes

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

    PRIORITY AND CONTRACTION:
        When we contract the belief base (remove a belief and its consequences),
        we need to decide which formulas to keep. We do this by computing
        'remainder sets' — maximal subsets that do not entail the removed formula.
        The selection function then picks the remainder sets that retain
        the highest priority formulas. This is what makes it a *partial meet* contraction.

    SYNTACTIC vs SEMANTIC membership:
        'p in B' checks if p is literally stored in the base (syntactic).
        'B entails p' checks if p logically follows from B (semantic).
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



