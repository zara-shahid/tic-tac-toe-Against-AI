import gradio as gr
import numpy as np

# 🧠 Game logic
def check_winner(board):
    for i in range(3):
        if abs(sum(board[i, :])) == 3:
            return board[i, 0]
        if abs(sum(board[:, i])) == 3:
            return board[0, i]
    if abs(sum(board.diagonal())) == 3:
        return board[0, 0]
    if abs(sum(np.fliplr(board).diagonal())) == 3:
        return board[0, 2]
    if not np.any(board == 0):
        return 0  # Draw
    return None

def ai_move(board):
    # Smart AI: try to win or block
    for player in [-1, 1]:
        for i in range(3):
            for j in range(3):
                if board[i, j] == 0:
                    board_copy = board.copy()
                    board_copy[i, j] = player
                    if check_winner(board_copy) == player:
                        return i, j
    if board[1, 1] == 0:
        return 1, 1
    for i, j in [(0,0),(0,2),(2,0),(2,2)]:
        if board[i,j]==0:
            return i,j
    open_cells = np.argwhere(board == 0)
    return tuple(open_cells[0])

def play(board_flat, r, c):
    board = np.array(board_flat).reshape(3, 3)
    if board[r, c] != 0:
        return board_flat, "🚫 Cell already taken! Try another.", board_flat

    board[r, c] = 1
    winner = check_winner(board)
    if winner == 1:
        return board.flatten().tolist(), "✅ You win!", board.flatten().tolist()
    elif winner == 0:
        return board.flatten().tolist(), "🤝 It's a draw!", board.flatten().tolist()

    ai_r, ai_c = ai_move(board)
    board[ai_r, ai_c] = -1
    winner = check_winner(board)
    if winner == -1:
        return board.flatten().tolist(), "🤖 AI wins!", board.flatten().tolist()
    elif winner == 0:
        return board.flatten().tolist(), "🤝 It's a draw!", board.flatten().tolist()

    return board.flatten().tolist(), "Your turn!", board.flatten().tolist()

def new_game():
    return [0]*9, "🎮 New game started! You go first."

def update_board_labels(board):
    labels = []
    for v in board:
        if v == 1:
            labels.append("❌")
        elif v == -1:
            labels.append("⭕")
        else:
            labels.append("⬜")
    return labels

# 🎨 Gradio interface
with gr.Blocks() as demo:
    board_state = gr.State([0]*9)

    status = gr.Markdown("### 🎮 New game started! You go first.")

    btns = []
    with gr.Column():
        for r in range(3):
            with gr.Row():
                for c in range(3):
                    btn = gr.Button("⬜", elem_id=f"cell-{r}-{c}", size="lg")
                    btns.append((btn, r, c))

    reset = gr.Button("🔄 Reset Game")

    for btn, r, c in btns:
        def on_click(board_flat, r=r, c=c):
            board, msg, _ = play(board_flat, r, c)
            return board, msg, board

        btn.click(
            on_click,
            inputs=[board_state],
            outputs=[board_state, status, board_state],
        ).then(
            update_board_labels,
            inputs=board_state,
            outputs=[b for b, _, _ in btns]
        )

    reset.click(
        new_game,
        outputs=[board_state, status]
    ).then(
        update_board_labels,
        inputs=board_state,
        outputs=[b for b, _, _ in btns]
    )

demo.launch()
