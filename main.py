
import tkinter as tk
import pickle
import random   

with open("q_table.pkl", "rb") as file:
    Q = pickle.load(file)

# ----------------------------
# Game setup
# ----------------------------

root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("420x500")
root.resizable(False, False)

board = [""] * 9
buttons = []
game_over = False

# ----------------------------
# Status label
# ----------------------------

status = tk.Label(
    root,
    text="Your turn (X)",
    font=("Arial", 18, "bold")
)
status.pack(pady=15)

# ----------------------------
# Check game result
# ----------------------------

def check_winner():
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None

# ----------------------------
# AI move (temporary random AI)
# ----------------------------

"""def find_winning_move(mark):
    for i in range(9):
        if board[i] == "":
            board[i] = mark
            result = check_winner()
            board[i] = ""

            if result == mark:
                return i

    return None"""




def ai_move():
    global game_over

    available = [i for i in range(9) if board[i] == ""]

    if not available:
        return

    state = tuple(board)

    q_values = [
    Q.get((tuple(board), "O", i), 0.0)
    for i in available
]
    print("\n--- AI BRAIN ---")

    for move, value in zip(available, q_values):
        print(f"Square {move + 1}: Q-value = {value:.4f}")

    print("----------------\n")

    best_value = max(q_values)

    best_moves = [
        i for i, value in zip(available, q_values)
        if value == best_value
    ]

    move = random.choice(best_moves)
    print(f"AI selected square: {move + 1}")

    board[move] = "O"
    buttons[move].config(text="O", state="disabled")

    result = check_winner()

    if result is not None:
        finish_game(result)
    else:
        status.config(text="Your turn (X)")



# ----------------------------
# Handle player move
# ----------------------------

def handle_click(index):
    global game_over

    if game_over or board[index] != "":
        return

    board[index] = "X"
    buttons[index].config(text="X", state="disabled")

    result = check_winner()

    if result:
        finish_game(result)
    else:
        status.config(text="AI is thinking...")
        root.after(350, ai_move)

# ----------------------------
# End game
# ----------------------------

def finish_game(result):
    global game_over

    game_over = True

    if result == "Draw":
        status.config(text="It's a draw!")
    elif result == "X":
        status.config(text="You win!")
    else:
        status.config(text="AI wins!")

    for button in buttons:
        button.config(state="disabled")

# ----------------------------
# Restart game
# ----------------------------

def restart_game():
    global board, game_over

    board = [""] * 9
    game_over = False

    for button in buttons:
        button.config(text="", state="normal")

    status.config(text="Your turn (X)")

# ----------------------------
# Create the 3x3 GUI
# ----------------------------

frame = tk.Frame(root)
frame.pack(expand=True)

for i in range(9):
    button = tk.Button(
        frame,
        text="",
        font=("Arial", 28, "bold"),
        width=5,
        height=2,
        command=lambda i=i: handle_click(i)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=4,
        pady=4
    )

    buttons.append(button)

# ----------------------------
# Restart button
# ----------------------------

restart_button = tk.Button(
    root,
    text="Restart Game",
    font=("Arial", 12),
    command=restart_game
)
restart_button.pack(pady=15)

root.mainloop()
