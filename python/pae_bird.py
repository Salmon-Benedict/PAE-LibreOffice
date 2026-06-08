import os
import json
import urllib.request
import urllib.error
import unohelper
from com.sun.star.sheet import XAddIn

FREE_API_KEY = "pae-free-public-2026"
API_URL = "https://pae-api-production.up.railway.app"
UPGRADE_URL = "https://salmon-benedict.github.io/pae-bird-landing/register.html"

def _config_path():
    config_dir = os.path.join(os.path.expanduser("~"), ".config", "paebird")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "key.txt")

def _get_api_key():
    try:
        with open(_config_path(), "r") as f:
            key = f.read().strip()
            if key:
                return key
    except OSError:
        pass
    return FREE_API_KEY

def _call_api(endpoint, payload):
    key = _get_api_key()
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/{endpoint}",
        data=data,
        headers={"Content-Type": "application/json", "x-api-key": key},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
            return body.get("result", "Error: no result")
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return f"Free tier limit reached — upgrade at {UPGRADE_URL}"
        if e.code == 401:
            return "Error: invalid API key — check Tools > PAE Bird Settings"
        return f"Error: HTTP {e.code}"
    except Exception as e:
        return f"Error: {e}"


class PaeBirdAddin(unohelper.Base, XAddIn):

    def __init__(self, ctx):
        self.ctx = ctx

    # XAddIn
    def getProgrammaticFuntionName(self, display_name):
        return display_name

    def getDisplayFunctionName(self, programmatic_name):
        return programmatic_name

    def getFunctionDescription(self, programmatic_name):
        descs = {
            "PAE_SOLVE": "Solve a polynomial equation",
            "PAE_EXPAND": "Expand a polynomial expression",
            "PAE_FACTOR": "Factor a polynomial expression",
            "PAE_DIFFERENTIATE": "Differentiate a polynomial expression",
            "PAE_INTEGRATE": "Integrate a polynomial expression",
        }
        return descs.get(programmatic_name, "")

    def getDisplayArgumentName(self, programmatic_name, index):
        args = {
            "PAE_SOLVE": ["expression"],
            "PAE_EXPAND": ["expression"],
            "PAE_FACTOR": ["expression"],
            "PAE_DIFFERENTIATE": ["expression", "variable"],
            "PAE_INTEGRATE": ["expression", "variable"],
        }
        names = args.get(programmatic_name, [])
        return names[index] if index < len(names) else ""

    def getArgumentDescription(self, programmatic_name, index):
        return ""

    def getProgrammaticCategoryName(self, programmatic_name):
        return "Add-In"

    def getDisplayCategoryName(self, category_name):
        return category_name

    # Calc functions
    def PAE_SOLVE(self, expression):
        return _call_api("solve", {"expression": expression})

    def PAE_EXPAND(self, expression):
        return _call_api("expand", {"expression": expression})

    def PAE_FACTOR(self, expression):
        return _call_api("factor", {"expression": expression})

    def PAE_DIFFERENTIATE(self, expression, variable):
        return _call_api("differentiate", {"expression": expression, "variable": variable})

    def PAE_INTEGRATE(self, expression, variable):
        return _call_api("integrate", {"expression": expression, "variable": variable})


def createInstance(ctx):
    return PaeBirdAddin(ctx)

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    PaeBirdAddin,
    "com.paebird.PaeBirdAddin",
    ("com.sun.star.sheet.AddIn",),
)
