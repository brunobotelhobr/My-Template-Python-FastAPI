"""General API Constants."""
import toml

#General Constants
app_name = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
app_version = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
website = toml.load("pyproject.toml")["tool"]["poetry"]["repository"]


# API Initialization parameters
start: dict[str, any] = {"title": app_name, "version": app_version,
                         "description": "API for the " + app_name + " application.",
                         "debug": env.local.is_debug,
                         "license_info": {"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
                         "contact": {"name": "Bruno Botelho", "url": website, "email": "bruno.botelho.br@gmail.com"}
                         }

if env.local.is_debug is True:
    start["redoc_url"] = "/redoc"
    start["openapi_url"] = "/openapi.json"
    start["docs_url"] = "/"
else:
    start["redoc_url"] = None
    start["openapi_url"] = None
    start["docs_url"] = None
