import json
import urllib.request
import urllib.error
import unohelper

from com.sun.star.sheet import XAddIn

# Served LOCALLY by PAE Bird.app now (see PolySwift/Poly/Poly/LocalServer.
# swift), not the internet -- no API key needed for a localhost-only
# listener. Existing already-installed copies of this add-in (the old,
# internet-based build) are unaffected -- LibreOffice extensions don't
# self-update, so this only changes what a fresh .oxt install gets.
# https, not http -- LocalServer.swift serves TLS with a per-machine
# certificate CertificateManager.swift generates and trusts on first
# launch (needed so browser-hosted callers aren't blocked as Mixed
# Content; urllib here isn't itself affected, but the contract is shared
# with functions.ts/taskpane.ts, which are).
API_URL = "https://127.0.0.1:51823"

# Standardizes on the same general /compute route (cmd/arg/expression ->
# result) PAE Bird.app's local server and Excel's client both use, rather
# than PAE-API's separate /solve, /expand, /factor, etc. legacy routes --
# those exist there only for older callers' backward compatibility; the
# local server doesn't carry that burden, so one route is simpler to keep
# in sync than six.
def _call_api(cmd, expression, variable=None):
    payload = {"cmd": cmd, "arg": variable or "", "expression": expression}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API_URL}/compute",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read())
            return body.get("result", "Error: no result")
    except urllib.error.URLError:
        return "Error: couldn't reach PAE Bird -- make sure the PAE Bird app is open on this Mac."
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
        return _call_api("solve", expression)

    def PAE_EXPAND(self, expression):
        return _call_api("expand", expression)

    def PAE_FACTOR(self, expression):
        return _call_api("factor", expression)

    def PAE_DIFFERENTIATE(self, expression, variable):
        return _call_api("differentiate", expression, variable)

    def PAE_INTEGRATE(self, expression, variable):
        return _call_api("integrate", expression, variable)


def createInstance(ctx):
    return PaeBirdAddin(ctx)

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    PaeBirdAddin,
    "com.paebird.PaeBirdAddin",
    ("com.sun.star.sheet.AddIn",),
)
