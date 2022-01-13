from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.painting import Painting

@app.route('/dashboard')
def paintings():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.get_by_id(data), paintings=Painting.get_all_paintings_with_users())

@app.route('/show/<int:painting_id>')
def show_one(painting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    data = {
        'id': painting_id
    }
    return render_template('show.html', user=User.get_by_id(user_data), painting=Painting.get_one_painting_with_users(data))

@app.route('/new')
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('create.html')

@app.route('/new/painting', methods = ['POST'])
def create_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect(f'/new')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'price' : request.form['price'],
        'creator_id' : session['user_id']
    }
    Painting.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:painting_id>')
def edit_painting(painting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":painting_id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_painting.html", painting=Painting.get_one(data),user=User.get_by_id(user_data))


@app.route('/edit/<int:painting_id>/update', methods=['POST'])
def update_painting(painting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect(f'/edit/{painting_id}')
    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'price' : request.form['price'],
        'creator_id' : session['user_id'],
        'id' : painting_id
    }
    painting = Painting.update_painting(data)
    return redirect('/dashboard')

@app.route('/destroy/painting/<int:id>')
def destroy_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Painting.destroy(data)
    return redirect('/dashboard')