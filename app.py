from flask import Flask, request, render_template, redirect, session, jsonify
from boggle import Boggle

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'coolcode' # set a 'SECRET_KEY' to enable the Flask session cookies

boggle_game = Boggle()

@app.route('/')
def home_page():
    """basic home page for boggle. Includes explanation of rules."""
    return render_template('home.html')

@app.route('/board')
def board_page():
    """Renders the boggle game-board"""
    if not is_board_valid(session.get('current_board')):
        #If board is invalid or non-existant, make a new one.
        current_board = boggle_game.make_board()
        session['current_board'] = current_board
    else:
        current_board = session['current_board']
        
    return render_template('board.html', boggle_board=current_board)

def is_board_valid(board):
    """Verifies the board is a 5x5 2d list of single upper-case characters."""

    if board == None or not isinstance(board, list) or len(board) != 5:
        return False
    else:
        for row in board:
            if not isinstance(row, list) or len(row) != 5:
                return False
            else:
                for cell in row:
                    if not isinstance(cell, str) or len(cell) != 1 or not cell.isalpha() or not cell.isupper():
                        return False                     
    return True


@app.route('/submit', methods=["POST"])
def submit_guess():
    """Checks guess against word list and responds with the result."""
    word = request.form.get('guess')
    info = jsonify({"result": boggle_game.check_valid_word(session['current_board'], word)})
    return info


@app.route('/records', methods=["POST"])
def record_stats():
    """Records the high score and total times played."""

    if session.get('highScore') == None:
        session['highScore'] = 0
    if session.get('highScore') < request.json['score']:
        session['highScore'] = request.json['score']


    if session.get("totalPlays") == None:
        session['totalPlays'] = 1
    else:
        session['totalPlays'] += 1

    return jsonify({ 'totalPlays': session['totalPlays'] })
