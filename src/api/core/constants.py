"""General API Constants."""
from typing import Any

import toml

from api.core.environment import running_environment

# General Constants
app_name = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
app_website = toml.load("pyproject.toml")["tool"]["poetry"]["repository"]


# API Initialization parameters
app_start_parameters: dict[str, Any] = {
    "title": app_name,
    "version": app_version,
    "description": "API for the " + app_name + " application.",
    "debug": running_environment.local.is_debug,
    "license_info": {"name": "MIT", "database_connection_url": "https://opensource.org/licenses/MIT"},
    "contact": {"name": "Bruno Botelho", "database_connection_url": app_website, "email": "bruno.botelho.br@gmail.com"},
}

if running_environment.local.is_debug is True:
    app_start_parameters["redoc_url"] = "/redoc"
    app_start_parameters["openapi_url"] = "/openapi.json"
    app_start_parameters["docs_url"] = "/"
else:
    app_start_parameters["redoc_url"] = None
    app_start_parameters["openapi_url"] = None
    app_start_parameters["docs_url"] = None
