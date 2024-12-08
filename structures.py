my_list = ['dog', 'cat', 'frog', 'cat', 'dog']  # список
# print(my_list)
# my_list = set(my_list)
# print(my_list)
# my_list[2] = 'wolf'
# print(my_list)
my_tuple = ('apple', 'potato', 'egg')  # кортеж и он не пополняемый, не изменяемый
# print(my_tuple[0])
my_set = {"mama", "dad", "grandma", "granddad", "dad"}  # множества хранят уникальное и не имеют порядка

# print(my_set)
my_dict = {
    "marketolog": ['33333', '44444'],
    "worker": 22222,
    'menager': 300000,
    'electric': 200000
}


def get(some_dct, key):
    print(f"Ваш элемент под ключом {key}: {some_dct[key]}")


get(my_dict, "electric")
