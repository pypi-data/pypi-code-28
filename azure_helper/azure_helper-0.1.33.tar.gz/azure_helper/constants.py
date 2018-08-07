class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[0;31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Headers
def basicHeader(apim):
    return {"Content-Type": "application/json",
            "Authorization": apim.token}


def basicPutPatchHeader(apim):
    return {"Content-Type": "application/json",
            "Authorization": apim.token,
            "If-Match": "*"}


def xmlHeader(apim):
    return {"Content-Type": "application/xml",
            "Authorization": apim.token}
