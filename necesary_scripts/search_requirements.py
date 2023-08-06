def delete_repetitive_characters(lista: list) -> list:
    nueva_lista = list(set(lista))
    return nueva_lista


def get_coincidences(element_list: list, search: list) -> int:
    count_number = 0
    for element in search:
        if element.lower() in element_list:
            count_number += 1

    return count_number
