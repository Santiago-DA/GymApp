from enum import Enum

class METs(Enum):
    EJERCISIO_LIGERO = (4,"Entrenamiento ligero")
    EJERCISIO_MEDIO = (5,"Entrenamiento medio")
    EJERCISIO_INTENSO = (6,"Entrenamiento intenso")
    BICICLETA = (7.4,"Bicicleta")
    CIRCUITO = (8,"Circuito")
if __name__ == "__main__":
    x = METs.BICICLETA
    print(x.value[1])
