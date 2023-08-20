from random import shuffle


def generate_dominoes() -> list:
    duplicated_dominoes = []
    for i in range(7):
        for j in range(7):
            duplicated_dominoes.append(sorted([i, j]))

    dominoes = []
    for d in duplicated_dominoes:
        if d not in dominoes:
            dominoes.append(d)

    return dominoes

def finding_first_player(first_player: list, second_player) -> list:
    fp_max = max(first_player)
    sp_max = max(second_player)

    if fp_max > sp_max:
        return first_player.pop(first_player.index(fp_max))
    elif fp_max < sp_max:
        return second_player.pop(second_player.index(sp_max))
    else:
        return []

def start_deal(stock: list) -> (list, list, list, list):
    duplicate_trigger = False

    while not duplicate_trigger:
        deal_stock = stock
        shuffle(deal_stock)
        first_player, second_player = [], []

        for _ in range(7):
            current_pop = deal_stock.pop()
            if current_pop[0] == current_pop[1]:
                duplicate_trigger = True
            first_player.append(current_pop)

            current_pop = deal_stock.pop()
            if current_pop[0] == current_pop[1]:
                duplicate_trigger = True
            second_player.append(current_pop)

        start_domino = finding_first_player(first_player, second_player)
        if not start_domino:
            duplicate_trigger = False

    return first_player, second_player, deal_stock, start_domino


if __name__ == "__main__":
    computer_pieces, player_pieces, stock_pieces, domino_snake = start_deal(generate_dominoes())
    if len(computer_pieces) > len(player_pieces):
        start_player = 'computer'
    else:
        start_player = 'player'

    print("Stock pieces:", stock_pieces)
    print("Computer pieces:", computer_pieces)
    print("Player pieces:", player_pieces)
    print("Domino snake:", [domino_snake])
    print("Status:", start_player)
