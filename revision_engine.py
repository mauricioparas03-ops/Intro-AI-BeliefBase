# AGM Operations
# Purpose: Modifies the Belief Base
# Components:
#   Expand: adds a formula to the set
#   Contract: uses inference engine to check for entailment, and removes formulas until the target is no logner entailed
#   Revise: combines the Expand and Contract (Levi identity? contract the negation, then expand)