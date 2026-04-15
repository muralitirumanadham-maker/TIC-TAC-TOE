import tkinter as tk
import random
import math
import winsound  # For sound (Windows). If error, remove this.

# ================== GAME LOGIC ==================
board = [" " for _ in range(9)]
buttons = []
current_difficulty = "Hard"

# Sound function
def play_click():
    try:
        winsound.Beep(800, 100)
    except:
        pass

# Check winner
def check_winner(b, player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(b[i] == player for i in combo) for combo in wins)

def is_draw():
    return " " not in board

# ================== AI ==================

def minimax(b, is_max):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if " " not in b:
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = " "
                best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = " "
                best = min(score, best)
        return best

def ai_move():
    if current_difficulty == "Easy":
        move = random.choice([i for i in range(9) if board[i] == " "])

    elif current_difficulty == "Medium":
        if random.random() < 0.5:
            move = random.choice([i for i in range(9) if board[i] == " "])
        else:
            move = best_move()

    else:  # Hard
        move = best_move()

    board[move] = "O"
    update_button(move, "O")

def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ================== UI ==================

def update_button(i, player):
    buttons[i]["text"] = player
    buttons[i]["state"] = "disabled"
    animate_button(buttons[i])

def animate_button(btn):
    # Simple animation effect
    def grow(size=10):
        if size <= 20:
            btn.config(font=("Arial", size, "bold"))
            root.after(20, lambda: grow(size+2))
    grow()

def player_click(i):
    if board[i] != " ":
        return

    play_click()
    board[i] = "X"
    update_button(i, "X")

    if check_winner(board, "X"):
        status_label.config(text="🎉 You Win!")
        disable_all()
        return

    if is_draw():
        status_label.config(text="😐 Draw!")
        return

    root.after(500, ai_turn)

def ai_turn():
    ai_move()

    if check_winner(board, "O"):
        status_label.config(text="🤖 AI Wins!")
        disable_all()
        return

    if is_draw():
        status_label.config(text="😐 Draw!")

def disable_all():
    for btn in buttons:
        btn["state"] = "disabled"

def reset_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text="", state="normal", font=("Arial", 14))
    status_label.config(text="Your Turn (X)")

def set_difficulty(level):
    global current_difficulty
    current_difficulty = level
    status_label.config(text=f"Difficulty: {level} | Your Turn")

# ================== MAIN WINDOW ==================

root = tk.Tk()
root.title("🎮 Tic Tac Toe AI")
root.geometry("350x450")
root.config(bg="#1e1e1e")

# Title
title = tk.Label(root, text="Tic Tac Toe", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Status
status_label = tk.Label(root, text="Your Turn (X)", font=("Arial", 12), bg="#1e1e1e", fg="lightgreen")
status_label.pack()

# Board frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 14), width=5, height=2,
                    command=lambda i=i: player_click(i),
                    bg="#2c2c2c", fg="white", activebackground="#444")
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Controls
control_frame = tk.Frame(root, bg="#1e1e1e")
control_frame.pack(pady=10)

tk.Button(control_frame, text="Easy", command=lambda: set_difficulty("Easy")).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="Medium", command=lambda: set_difficulty("Medium")).grid(row=0, column=1, padx=5)
tk.Button(control_frame, text="Hard", command=lambda: set_difficulty("Hard")).grid(row=0, column=2, padx=5)

tk.Button(root, text="Restart 🔄", command=reset_game, bg="orange").pack(pady=10)

root.mainloop()