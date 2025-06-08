from flask import Flask, render_template, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = 'golospro123'

polls = [
    {
        'id': str(uuid.uuid4()),
        'question': 'Лучший язык программирования?',
        'options': [{'text': 'Python', 'votes': 0}, {'text': 'JavaScript', 'votes': 0}]
    }
]

ADMIN_PASSWORD = 'admin123'


@app.route('/')
def home():
    return render_template('index.html', polls=polls)


@app.route('/poll/<poll_id>', methods=['GET', 'POST'])
def poll(poll_id):
    poll = next((p for p in polls if p['id'] == poll_id), None)
    if not poll:
        return "Голосование не найдено", 404

    if request.method == 'POST':
        if 'option' in request.form:
            option_index = int(request.form['option'])
            if 0 <= option_index < len(poll['options']):
                poll['options'][option_index]['votes'] += 1
                return redirect(url_for('poll', poll_id=poll_id))
            else:
                return "Неверный выбор", 400
        return "Выберите вариант", 400

    total_votes = sum(option['votes'] for option in poll['options'])
    labels = [option['text'] for option in poll['options']]
    data = [option['votes'] for option in poll['options']]
    percentages = [round((vote / total_votes * 100 if total_votes > 0 else 0), 1) for vote in data]
    colors = ["#bf4c4c", "#0040ff", "#00ff0d", "#ff00ea", "#00bbff", "#d0ff00", "#c3d0ff", "#ff8c00"][:len(labels)]

    return render_template('poll.html', poll=poll, labels=labels, data=data, percentages=percentages, colors=colors)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin' not in session:
        if request.method == 'POST':
            if request.form['password'] == ADMIN_PASSWORD:
                session['admin'] = True
                return redirect(url_for('admin'))
            return render_template('admin_login.html', error="Неверный пароль")
        return render_template('admin_login.html', error=None)

    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options')
        if question and all(options):
            polls.append({
                'id': str(uuid.uuid4()),
                'question': question,
                'options': [{'text': opt, 'votes': 0} for opt in options]
            })
        return redirect(url_for('admin'))

    return render_template('admin.html', polls=polls)


@app.route('/delete_poll/<poll_id>', methods=['POST'])
def delete_poll(poll_id):
    if 'admin' in session:
        global polls
        polls = [p for p in polls if p['id'] != poll_id]
    return redirect(url_for('admin'))


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
