from random import shuffle, choice
from itertools import cycle


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
    """Finding the start player."""
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

    return player_one, player_two, dominoes, [start_domino]


def current_game_status(computer_pieces: list, user_pieces: list, stock_pieces: list, domino_snake: list) -> None:
    """Current game status."""
    print('=' * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()

    if len(domino_snake) < 7:
        print(*domino_snake, sep='')
    else:
        print(*domino_snake[:3], '...',  *domino_snake[-3:], sep='')
    print()

    print("Your pieces:")
    for i, d in enumerate(user_pieces, start=1):
        print(f'{i}:{d}')
    print()


def computer_turn(computer_pieces: list, domino_snake: list, stock_pieces: list) -> int:
    """Computer turn."""
    user_input = input("Status: Computer is about to make a move. Press Enter to continue...\n")
    computer_inputs = [i * j for i in range(1, len(computer_pieces)) for j in (-1, 1)]
    shuffle(computer_inputs)
    computer_input = 0
    for i in computer_inputs:
        if i > 0 and domino_snake[-1][-1] in computer_pieces[abs(i)]:
            place_domino(i + 1, computer_pieces, domino_snake)
            computer_input = i
            break
        elif i < 0 and domino_snake[0][0] in computer_pieces[abs(i)]:
            place_domino(i - 1, computer_pieces, domino_snake)
            computer_input = i
            break
    else:
        if stock_pieces:
            get_domino(computer_pieces, stock_pieces)
        computer_input = 0
    return computer_input


def user_turn(user_pieces: list, domino_snake: list, stock_pieces: list) -> int:
    """User turn."""
    print("Status: It's your turn to make a move. Enter your command.")
    while True:
        user_input = input()
        if user_input.lstrip('-').isdigit():
            user_input = int(user_input)
            if abs(user_input) <= len(user_pieces):
                if user_input == 0:
                    if stock_pieces:
                        get_domino(user_pieces, stock_pieces)
                    return user_input
                elif user_input > 0 and domino_snake[-1][-1] in user_pieces[abs(user_input)-1]:
                    place_domino(user_input, user_pieces, domino_snake)
                    return user_input
                elif user_input < 0 and domino_snake[0][0] in user_pieces[abs(user_input)-1]:
                    place_domino(user_input, user_pieces, domino_snake)
                    return user_input
                else:
                    print("Illegal move. Please try again.")
            else:
                print("Invalid input. Please try again.")
        else:
            print("Invalid input. Please try again.")


def place_domino(player_input: int, player_pieces: list, domino_snake: list) -> None:
    """Placing domino in a snake."""
    piece = player_pieces[abs(player_input)-1]
    if player_input > 0:
        if domino_snake[-1][-1] != piece[0]:
            piece.reverse()
        domino_snake.append(player_pieces.pop(player_input-1))
    else:
        if domino_snake[0][0] != piece[1]:
            piece.reverse()
        domino_snake.insert(0, player_pieces.pop(abs(player_input) - 1))


def get_domino(player_pieces: list, stock_pieces: list) -> None:
    """Getting domino from stock."""
    player_pieces.append(stock_pieces.pop())


def end_game_check(computer_pieces: list, user_pieces: list, domino_snake: list, last_computer_turn: int, last_user_turn: int, stock_pieces: list) -> bool:
    """Checking the end of the game"""
    if len(computer_pieces) == 0:
        print("Status: The game is over. The computer won!")
        return True
    elif len(user_pieces) == 0:
        print("Status: The game is over. You won!")
        return True

    if len(domino_snake) > 6 and domino_snake[0][0] == domino_snake[-1][-1]:
        sought_number = domino_snake[0][0]
        sought_number_amount = 0
        for i in domino_snake:
            for j in i:
                if j == sought_number:
                    sought_number_amount += 1
        if sought_number_amount == 8:
            print("Status: The game is over. It's a draw!")
            return True

    if (not stock_pieces) and last_user_turn == last_computer_turn == 0:
        print("Status: The game is over. It's a draw!")
        return True
    return False


if __name__ == "__main__":
    computer_pieces, user_pieces, stock_pieces, domino_snake = start_deal(generate_dominoes())

    players = ['computer', 'user']
    player_cycle = cycle(players)
    active_player = next(player_cycle)
    if len(computer_pieces) < len(user_pieces):
        active_player = next(player_cycle)

    last_computer_turn = 0
    last_user_turn = 0
    while True:
        current_game_status(computer_pieces, user_pieces, stock_pieces, domino_snake)

        if end_game_check(computer_pieces, user_pieces, domino_snake, last_computer_turn, last_user_turn, stock_pieces):
            break

        if active_player == 'computer':
            last_computer_turn = computer_turn(computer_pieces, domino_snake, stock_pieces)
        else:
            last_user_turn = user_turn(user_pieces, domino_snake, stock_pieces)

        active_player = next(player_cycle)
