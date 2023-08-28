from random import shuffle


def generate_dominoes() -> list:
    """Return domino pool."""
    duplicated_dominoes = []  # domino combinations with repetitions
    for i in range(7):
        for j in range(7):
            duplicated_dominoes.append(sorted([i, j]))

    dominoes = []  # clean domino pool (without repetitions)
    for d in duplicated_dominoes:
        if d not in dominoes:
            dominoes.append(d)

    return dominoes

def finding_start_domino(player_one: list, player_two: list) -> list:
    """Finding tht start player"""

    player_one_doubles = [d for d in player_one if d[0] == d[1]]
    player_two_doubles = [d for d in player_two if d[0] == d[1]]

    try:
        player_one_max_double = max(player_one_doubles)
    except ValueError:
        player_one_max_double = [-1, -1]
    try:
        player_two_max_double = max(player_two_doubles)
    except ValueError:
        player_two_max_double = [-1, -1]

    if player_one_max_double > player_two_max_double:
        return player_one.pop(player_one.index(player_one_max_double))
    else:
        return player_two.pop(player_two.index(player_two_max_double))

def start_deal(dominoes: list) -> (list, list, list, list):
    """Distribution of start hands.
    Return: first player hand, second player hand, stock, start domino
    """
    player_double_exist = False

    while not player_double_exist:
        shuffle(dominoes)
        player_one, player_two = [], []

        for _ in range(7):
            current_pop = dominoes.pop()
            if current_pop[0] == current_pop[1]:
                player_double_exist = True
            player_one.append(current_pop)

            current_pop = dominoes.pop()
            if current_pop[0] == current_pop[1]:
                player_double_exist = True
            player_two.append(current_pop)

        start_domino = finding_start_domino(player_one, player_two)

    return player_one, player_two, dominoes, start_domino


if __name__ == "__main__":
    computer_pieces, player_pieces, stock_pieces, domino_snake = start_deal(generate_dominoes())

    print('='*70)
    print('Stock size:', len(stock_pieces))
    print('Computer pieces:', len(computer_pieces))
    print()
    print(domino_snake)
    print()
    print('Your pieces:')
    for i, d in enumerate(player_pieces, start=1):
        print(f'{i}:{d}')
    print()
    if len(computer_pieces) > len(player_pieces):
        print("Status: Computer is about to make a move. Press Enter to continue...")
    else:
        print("Status: It's your turn to make a move. Enter your command.")
