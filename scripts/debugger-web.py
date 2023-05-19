"""Debugger for local development."""  # type: ignore
import sys
import web_pdb

sys.path.insert(0, 'src/api/')

from api.main import run

BIND_ADDRESS = "0.0.0.0"
BIND_PORT_DEBBUGER = 12345

# Set tracer
web_pdb.set_trace(host=BIND_ADDRESS, port=BIND_PORT_DEBBUGER)

# Run the app
breakpoint()
run()