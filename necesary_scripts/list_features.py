def sort(list: list, reverse: bool) -> None:
    for i in range(len(list)):
        for a in range(0, i):
            if list[i][0] < list[a][0] and not reverse:
                list.insert(list.index(list[a]), list[i])
                del list[i + 1]
            elif list[i][0] > list[a][0] and reverse:
                list.insert(list.index(list[a]), list[i])
                del list[i + 1]

        # list.sort(key=lambda element: element[1], reverse=reverse)


def separate_by_vowels(string: str) -> list:
    ultimo = 0
    lista = []
    vowels = ["a", "e", "i", "o", "u"]
    for i in range(len(string)):
        if string[i] in vowels:
            lista.append(string[ultimo:i + 1].replace(" ", ""))
            ultimo = i + 1

    return lista


# Es reemplazable por un filter: filter(lambda x: x.isdigit(), list)
def separate_by_numbers(string: str) -> list:
    lista = list(filter(lambda x: x.isdigit(), string))
    # for i in string:
    #   if i.isdigit():
    #     list.append(i)
    return lista


def converted_to_list(string: str) -> list:
    lista = [string]
    return lista


def get(list: list, search: str) -> str:
    for value in list:
        if search == value.id:
            return value
