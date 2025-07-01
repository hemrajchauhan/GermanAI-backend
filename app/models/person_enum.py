from enum import Enum

class Person(str, Enum):
    ich = "ich"
    du = "du"
    er_sie_es = "er/sie/es"
    wir = "wir"
    ihr = "ihr"
    sie_Sie = "sie/Sie"
