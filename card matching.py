import os
import random
import time

ROWS = 4
COLS = 4
TOTAL = ROWS * COLS
PAIRS = TOTAL // 2

SYMBOLS = ["🍎", "🍊", "🍋", "🍇", "🍓", "🍒", "🍉", "🍕"]


class Card:
    def __init__(self, symbol_id):
        self.symbol_id = symbol_id
        self.revealed = False



def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def init_board():
    """Create a shuffled ROWS x COLS board of Card objects."""
    ids = [i // 2 for i in range(TOTAL)]   
    random.shuffle(ids)

    board = []
    k = 0
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(Card(ids[k]))
            k += 1
        board.append(row)
    return board


def print_board(board, moves, matches, flip1=None, flip2=None):
    clear_screen()
    print("\n  ╔══════════════════════════════════════╗")
    print("  ║      MEMORY MATCHING CARD GAME       ║")
    print("  ╚══════════════════════════════════════╝\n")

    print("       " + "".join(f"  {c + 1}  " for c in range(COLS)))
    print("      " + "──────" * COLS)

    for r in range(ROWS):
        line = f"   {r + 1}  │"
        for c in range(COLS):
            card = board[r][c]
            show = (
                card.revealed
                or (flip1 == (r, c))
                or (flip2 == (r, c))
            )
            symbol = SYMBOLS[card.symbol_id] if show else "░░"
            line += f"  {symbol}  "
        print(line)

    print("      " + "──────" * COLS)
    print(f"\n  Moves: {moves:<4}   Matches: {matches} / {PAIRS}\n")


def get_card(board, prompt):
    """
    Prompt the player for a row/col pair.
    Returns a (row, col) tuple, 0-indexed, for an unrevealed card.
    """
    while True:
        raw = input(f"  {prompt} (row col, e.g. 2 3): ").strip()
        parts = raw.split()

        if len(parts) != 2 or not all(p.lstrip("-").isdigit() for p in parts):
            print("  ✗  Invalid input – enter two numbers.")
            continue

        r, c = int(parts[0]), int(parts[1])

        if not (1 <= r <= ROWS) or not (1 <= c <= COLS):
            print(f"  ✗  Out of range – row 1-{ROWS}, col 1-{COLS}.")
            continue

        r -= 1
        c -= 1   

        if board[r][c].revealed:
            print("  ✗  That card is already matched – pick another.")
            continue

        return (r, c)



def play(board):
    moves = 0
    matches = 0

    while matches < PAIRS:
        print_board(board, moves, matches)
        r1, c1 = get_card(board, "Pick 1st card")

        print_board(board, moves, matches, flip1=(r1, c1))

        while True:
            r2, c2 = get_card(board, "Pick 2nd card")
            if (r2, c2) != (r1, c1):
                break
            print("  ✗  Same card – choose a different one.")

        moves += 1

        print_board(board, moves, matches, flip1=(r1, c1), flip2=(r2, c2))
        time.sleep(0.9)

        card1, card2 = board[r1][c1], board[r2][c2]
        if card1.symbol_id == card2.symbol_id:
            card1.revealed = True
            card2.revealed = True
            matches += 1
            print(f"  ✔  Match!  {SYMBOLS[card1.symbol_id]}\n")
            time.sleep(0.7)
        else:
            print("  ✘  No match – try to remember those positions!\n")
            time.sleep(1.0)

    return moves


def win_screen(board, moves):
    print_board(board, moves, PAIRS)
    print("  ★  Congratulations!  You matched all pairs!")
    print(f"  ★  Total moves: {moves}")

    if moves <= PAIRS + 2:
        print("  ★  Rating: GENIUS! 🏆")
    elif moves <= PAIRS * 2:
        print("  ★  Rating: Great!  🥈")
    else:
        print("  ★  Rating: Good!   🥉")

    print()


def main():
    while True:
        board = init_board()
        moves = play(board)
        win_screen(board, moves)

        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("\n  Thanks for playing! 👋\n")


if __name__ == "__main__":
    main()
