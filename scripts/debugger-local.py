"""Debugger for local development."""  # type: ignore
import ipdb
import subprocess

# To call it manually: python -m ipdb src/api/main.py
print("----------------------------------------------------------------")
print("Debugging...")
print("----------------------------------------------------------------")   
print("   to set a breakpoint use: breakpoint()")
print("   h: Help.")
print("   n: Next.")
print("   s: Step In.")
print("   l: List.")
print("   ll: List More.")
print("   c: Continue.")
print("   pp vars(): Show Vars.")
print("   pp my-var: Show a Var.")
print("   where: Show chain of fuctions calls.")
print("   exit: Exit.")
print("----------------------------------------------------------------")

DEBUG_FILE = "src/api/main.py"
STOP_AT_BEGINNING = True

# Stop at the beginning of the file
if STOP_AT_BEGINNING:
    ipdb.set_trace()

# Run the file
subprocess.run(["python", DEBUG_FILE])
