from enum import Enum

class VerbForm(str, Enum):
    infinitiv = "infinitiv"
    praesens = "praesens"
    praeteritum = "praeteritum"
    perfekt = "perfekt"
    plusquamperfekt = "plusquamperfekt"
    futur1 = "futur1"
    futur2 = "futur2"
    konjunktiv1 = "konjunktiv1"
    konjunktiv2 = "konjunktiv2"
    imperativ = "imperativ"
    partizip1 = "partizip1"
    partizip2 = "partizip2"