# run_example.py
# Examples are from Week 10 Exercises

from knowledge_representation import BeliefBase, Atom
from inference_engine import entails
from revision_engine import contract

def run_tests():
    print("--- Testing Exercise 1: Logical Entailment ---")
    # KB = {~p -> q, q -> p, p -> r ^ s}
    # Test if p ^ r ^ s follows from KB.
    kb_ex1 = BeliefBase()
    
    # Define the atoms first based on knowledge_representation.py
    p = Atom('p')
    q = Atom('q')
    r = Atom('r')
    s = Atom('s')
    
    # Building formulas using operators (~, >>, &, |)
    kb_ex1.add(~p >> q)
    kb_ex1.add(q >> p)
    kb_ex1.add(p >> (r & s))
    
    test_formula = p & r & s
    
    # Using the 'entails' function from inference_engine.py
    result = entails(kb_ex1, test_formula)
    print(f"Does KB entail '{test_formula}'? \n {result}")
    
    
    print("\n--- Testing Exercise 2: Belief Contraction ---")
    # Belief Base A = {p, q, p & q, p | q, p -> q}
    # Contract with q.
    kb_ex2 = BeliefBase()
    
    # Adding formulas with priority weights
    kb_ex2.add(p, priority=5)
    kb_ex2.add(q, priority=4)
    kb_ex2.add(p & q, priority=3)
    kb_ex2.add(p | q, priority=2)
    kb_ex2.add(p >> q, priority=1)
    
    print(f"Original Belief Base: {kb_ex2.get_formulas()}")
    
    # Using the 'contract' function from revision_engine.py
    contract_formula = q
    new_kb = contract(kb_ex2, contract_formula)
    
    print(f"Belief Base after contracting '{contract_formula}': {new_kb.get_formulas()}")
    print("Expected possible outcomes: {p, p ∨ q}, {p → q}, {p ∨ q, p → q}, or {p ∨ q}")

if __name__ == "__main__":
    run_tests()