from Sprint.settings import CONSTS
from SprintLib.language import languages


def attributes(request):
    return {**CONSTS, "languages": sorted(languages, key=lambda x: x.name)}
