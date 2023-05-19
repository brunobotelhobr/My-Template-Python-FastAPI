"""Debugger for local development."""  # type: ignore
import ipdb
import subprocess
import sys
import uvicorn

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



sys.path.insert(0, 'src/api/')
from api.main import app  # type: ignore

BIND_ADDRESS = "0.0.0.0"
BIND_PORT_DEBBUGER = 12345
BIND_PORT_APP = 8000
DEBUG_FILE = "src/api/main.py"
STOP_AT_BEGINNING = True

# Stop at the beginning of the file
if STOP_AT_BEGINNING:
    ipdb.set_trace()

# Run the file
uvicorn.run(app=app, host=BIND_ADDRESS, port=BIND_PORT_APP)


exit()