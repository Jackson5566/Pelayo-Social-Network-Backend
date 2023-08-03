def delete_repetitive_characters(lista: list) -> list:
  nueva_lista = list(set(lista))
  return nueva_lista

def Coincidences(lista_elemento: list, busqueda: str) -> int:
  numero_contador = 0
  for elemento in busqueda:
    if elemento.lower() in lista_elemento:
      numero_contador += 1
  
  return numero_contador