
import streamlit as st

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="8 Queens AI Challenge",
    page_icon="♛",
    layout="wide"
)

# ---------------------------------
# INITIALIZE BOARD
# ---------------------------------
OPTIONS = ["Not placed"] + [
    f"Column {i}" for i in range(1, 9)
]

for row in range(8):
    key = f"row_{row}"
    if key not in st.session_state:
        st.session_state[key] = "Not placed"


# ---------------------------------
# AI BACKTRACKING ALGORITHM
# ---------------------------------
def solve_queens():
    board = [-1] * 8

    def is_safe(row, col):
        for previous_row in range(row):
            previous_col = board[previous_row]

            if previous_col == col:
                return False

            if abs(previous_col - col) == abs(previous_row - row):
                return False

        return True

    def backtrack(row):
        if row == 8:
            return True

        for col in range(8):
            if is_safe(row, col):
                board[row] = col

                if backtrack(row + 1):
                    return True

                board[row] = -1

        return False

    if backtrack(0):
        return board

    return None


# ---------------------------------
# BUTTON FUNCTIONS
# ---------------------------------
def reset_board():
    for row in range(8):
        st.session_state[f"row_{row}"] = "Not placed"


def show_solution():
    solution = solve_queens()

    if solution:
        for row in range(8):
            st.session_state[f"row_{row}"] = (
                f"Column {solution[row] + 1}"
            )


# ---------------------------------
# PAGE DESIGN
# ---------------------------------
st.title("♛ 8 Queens AI Challenge")

st.write(
    "Welcome to the 8 Queens Problem! "
    "Place 8 queens on the chessboard without "
    "allowing any two queens to attack each other."
)

st.info(
    "A queen can attack horizontally, vertically "
    "and diagonally."
)

st.divider()

# ---------------------------------
# GET PLAYER'S QUEEN POSITIONS
# ---------------------------------
st.subheader("Choose Your Queen Positions")

st.write("Select one column for each row.")

col1, col2 = st.columns(2)

for row in range(8):
    with col1 if row < 4 else col2:
        st.selectbox(
            f"Row {row + 1}",
            OPTIONS,
            key=f"row_{row}"
        )

# Convert selected positions into numbers
positions = []

for row in range(8):
    selected = st.session_state[f"row_{row}"]

    if selected == "Not placed":
        positions.append(-1)
    else:
        positions.append(int(selected.split()[-1]) - 1)


# ---------------------------------
# CHECK FOR ATTACKING QUEENS
# ---------------------------------
def find_conflicts(positions):
    conflicts = []

    for r1 in range(8):
        for r2 in range(r1 + 1, 8):

            c1 = positions[r1]
            c2 = positions[r2]

            if c1 == -1 or c2 == -1:
                continue

            if c1 == c2 or abs(c1 - c2) == abs(r1 - r2):
                conflicts.append((r1, r2))

    return conflicts


conflicts = find_conflicts(positions)
placed = sum(1 for col in positions if col != -1)

# ---------------------------------
# DISPLAY CHESSBOARD
# ---------------------------------
st.subheader("Your Chessboard")

conflict_rows = set()

for r1, r2 in conflicts:
    conflict_rows.add(r1)
    conflict_rows.add(r2)

board_html = """
<style>
.chessboard {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    max-width: 560px;
    width: 100%;
    border: 4px solid #333;
    margin: 15px auto;
}
.square {
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: clamp(20px, 5vw, 42px);
}
.light {
    background-color: #f0d9b5;
    color: #222;
}
.dark {
    background-color: #9b7653;
    color: white;
}
</style>
<div class="chessboard">
"""

for row in range(8):
    for col in range(8):

        color = "light" if (row + col) % 2 == 0 else "dark"

        if positions[row] == col:
            symbol = "♛"
        else:
            symbol = ""

        board_html += (
            f'<div class="square {color}">{symbol}</div>'
        )

board_html += "</div>"

st.markdown(board_html, unsafe_allow_html=True)

# ---------------------------------
# GAME STATUS
# ---------------------------------
st.write(f"**Queens placed:** {placed} / 8")

if conflicts:
    st.error(
        f"Conflict detected! {len(conflicts)} attacking pair(s). "
        "Try changing your positions."
    )

elif placed == 8:
    st.success(
        "Congratulations! You solved the 8 Queens Problem! 🎉"
    )

else:
    st.info(
        "Good progress! Continue placing your queens."
    )

# ---------------------------------
# ACTION BUTTONS
# ---------------------------------
st.divider()

button1, button2 = st.columns(2)

with button1:
    st.button(
        "🤖 Find AI Solution",
        use_container_width=True,
        on_click=show_solution
    )

with button2:
    st.button(
        "🔄 Reset Board",
        use_container_width=True,
        on_click=reset_board
    )

# ---------------------------------
# LEARNING SECTION
# ---------------------------------
st.divider()

st.subheader("🧠 How Does AI Solve This Problem?")

st.write("""
The AI uses a technique called Backtracking.

1. It starts from the first row.
2. It checks whether a queen can be placed safely.
3. It moves to the next row.
4. If a position causes a conflict, it goes back.
5. It tries another position.
6. It continues until all 8 queens are placed safely.

This is an example of a Constraint Satisfaction Problem (CSP).
""")

st.caption("AI Virtual Lab | 8 Queens Problem | Backtracking Algorithm")

