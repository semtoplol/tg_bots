# def peperoni():
#     return "стадартная пицца пеперони"

def decoratio(number):

    def peper(base_pizza):
        print(base_pizza(),' с добавкой перца')

    def tomato(base_pizza):
        print(base_pizza(), 'с добавкой томатов')

    def potato(base_pizza):
        print(base_pizza(), 'с добавкой жаренной картошкой')

    def chesee(base_pizza):
        print(base_pizza(), ' с добавкой сыра')

    if number == 1:
        return peper
    if number == 2:
        return tomato
    if number == 3:
        return potato
    if number == 4:
        return chesee

# decoratio(1)(peperoni)
@decoratio(2)
def peperoni():
    return "стадартная пицца пеперони"