from flask import Flask, render_template, redirect, url_for, session
from random import randint

app = Flask(__name__)
app.secret_key = 'some_secret'

def init_game(mode):
    session['character'] = None
    session['mode'] = mode
    session['wins'] = [0, 0]
    session['ties'] = 0
    session['round'] = 0
    session['max_round'] = 0
    session['prev_round'] = None
    session['choises'] = None
    session['style_choises'] = None
    session['result'] = None

@app.route('/')
def main():
    return redirect(url_for('game'))

@app.route('/home/character/<int:character>/')
def select_character(character):
    session['character'] = character
    return redirect(url_for('game'))

@app.route('/home/<mode>/choose_character/')
def init(mode):
    init_game(mode)
    return render_template('game.jinja2', data=dict(session))

@app.route('/choise/<int:choise>/')  
def choise(choise):
    session['choises'] = [choise]
    if session['character'] == 0:
        session['choises'].append(randint(0, 2))
    else:
        session['choises'].insert(0, randint(0, 2))
    return redirect(url_for('game'))

@app.route('/continue/')  
def continue_game():
    session['result'] = None
    session['prev_round'] = None
    if session['round'] > session['max_round']:
        session['max_round'] = session['round']
    return redirect(url_for('game'))

@app.route('/game/')
def game():
    if 'character' not in session or session['character'] is None:
        return redirect(url_for('init', mode=(session['mode'] if 'mode' in session and session['mode'] is not None else 'counted_ties')))
    if session['choises'] is not None:
        if session['choises'][0] == session['choises'][1]:
            if session['mode'] == 'counted_ties':
                session['ties'] += 1
            else:
                session['round'] += 1
            session['result'] = 0
        else:
            winner = -1
            if abs(session['choises'][0] - session['choises'][1]) == 1:
                winner = session['choises'].index(max(session['choises']))
            else:
                winner = session['choises'].index(min(session['choises']))
            session['wins'][winner] += 1
            session['prev_round'] = session['round'] + 1
            session['round'] = 0
            session['result'] = 1 if winner == session['character'] else 2
        session['style_choises'] = session['choises']
        session['choises'] = None

    return render_template('game.jinja2', data=dict(session))

@app.errorhandler(404)
def error404(e):
    return render_template('error404.jinja2')

if __name__ == "__main__":
    app.run(debug=True)
