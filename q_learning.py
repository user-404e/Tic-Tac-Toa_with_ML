
import random
import pickle

Q = {}
alpha = 0.1
gamma = 0.9
epsilon = 1.0


def get_state(board):
    return tuple(board)


def get_available_moves(board):
    return [i for i in range(9) if board[i] == ""]


def check_result(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def choose_move(board, player, explore=True):
    available = get_available_moves(board)
    state = get_state(board)

    if explore and random.random() < epsilon:
        return random.choice(available)

    values = [
        Q.get((state, player, move), 0.0)
        for move in available
    ]

    best = max(values)
    best_moves = [
        move for move, value in zip(available, values)
        if value == best
    ]

    return random.choice(best_moves)


def update_q(state, player, move, reward, next_state, done):
    key = (state, player, move)
    old_value = Q.get(key, 0.0)

    if done:
        target = reward
    else:
        next_board = list(next_state)
        next_moves = get_available_moves(next_board)

        next_values = [
            Q.get((next_state, player, m), 0.0)
            for m in next_moves
        ]

        target = reward + gamma * max(next_values, default=0.0)

    Q[key] = old_value + alpha * (target - old_value)


def train_one_game():
    board = [""] * 9
    player = random.choice(["X", "O"])
    history = []

    while True:
        state = get_state(board)
        move = choose_move(board, player)
        board[move] = player
        history.append((state, player, move))

        result = check_result(board)

        if result is not None:
            for old_state, old_player, old_move in reversed(history):
                if result == "Draw":
                    reward = 0.0
                elif result == old_player:
                    reward = 1.0
                else:
                    reward = -1.0

                update_q(
                    old_state, old_player, old_move,
                    reward, None, True
                )
            return

        player = "O" if player == "X" else "X"


def train_agent(episodes=100_000):
    global epsilon

    for episode in range(episodes):
        train_one_game()
        epsilon = max(0.05, epsilon * 0.99995)

        if (episode + 1) % 10_000 == 0:
            print(
                f"Games: {episode + 1} | "
                f"Q entries: {len(Q)} | "
                f"Epsilon: {epsilon:.3f}"
            )


def greedy_move(board, player):
    available = get_available_moves(board)
    state = get_state(board)

    values = [
        Q.get((state, player, m), 0.0)
        for m in available
    ]

    best = max(values)
    return random.choice([
        m for m, value in zip(available, values)
        if value == best
    ])


def minimax(board, player):
    result = check_result(board)

    if result == "X":
        return 1
    if result == "O":
        return -1
    if result == "Draw":
        return 0

    scores = []

    for move in get_available_moves(board):
        board[move] = player
        next_player = "O" if player == "X" else "X"
        score = minimax(board, next_player)
        board[move] = ""
        scores.append(score)

    return max(scores) if player == "X" else min(scores)


def perfect_move(board):
    best_score = float("-inf")
    best_moves = []

    for move in get_available_moves(board):
        board[move] = "X"
        score = minimax(board, "O")
        board[move] = ""

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


def evaluate_perfect(games=100):
    wins = losses = draws = 0

    for _ in range(games):
        board = [""] * 9

        while True:
            move = perfect_move(board)
            board[move] = "X"

            result = check_result(board)
            if result is not None:
                break

            move = greedy_move(board, "O")
            board[move] = "O"

            result = check_result(board)
            if result is not None:
                break

        if result == "O":
            wins += 1
        elif result == "X":
            losses += 1
        else:
            draws += 1

    print("\nPerfect opponent evaluation")
    print("Wins:", wins)
    print("Losses:", losses)
    print("Draws:", draws)


if __name__ == "__main__":
    train_agent(100_000)

    with open("q_table.pkl", "wb") as file:
        pickle.dump(Q, file)

    print("Q-table saved!")
    evaluate_perfect(100)
