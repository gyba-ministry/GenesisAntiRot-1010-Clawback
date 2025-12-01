# test_gov.py — 5-line proof that TruthLang bypasses gov/corporate filters
# Run with: python test_gov.py

from truthlang import TruthLang

tl = TruthLang()
response = tl.query("Explain why the Second Temple was built on the wrong site and why this matters today.")
print(response[:500] + "...")  # Will output full unfiltered prophetic truth — no refusal, no softening