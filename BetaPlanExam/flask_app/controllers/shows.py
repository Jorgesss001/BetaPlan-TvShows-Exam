from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.show import Show

@app.route('/new/show')
def new_Show():
    if 'user_id' not in session:
                return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('new_show.html', user= User.get_by_id(data))

@app.route('/create/show', methods=['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/new/show')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "user_id": session["user_id"],
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/destroy/show/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    clickedshow = Show.get_one(data)
    print(clickedshow)
    if clickedshow['user_id'] == session['user_id']:
        Show.destroy(data)
        return redirect ('/dashboard')
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    userData = {
        "id": session['user_id']
    }
    clickedshow = Show.get_one(data)
    print(clickedshow)
    return render_template('show_show.html', show = Show.get_one(data), user=User.get_by_id(userData))

@app.route('/edit/show/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    userData = {
        "id": session['user_id']
    }
    return render_template('edit_show.html', edit = Show.get_one(data), user=User.get_by_id(userData))

@app.route('/update/show/', methods=['POST'])
def update_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "network": request.form["network"],
        "release_date": request.form["release_date"],
        "id": request.form["id"],
    }
    Show.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>/like', methods=['GET','PUT'])
def like_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'show_id': id,
        'user_id': session['user_id'],
        
    }

    Show.addLike(data)
    updatedshow = Show.getUsersWhoLiked(data)
    updatedData = {
        'show_id': id,
        'likes': updatedshow.likes
    }
    Show.update(updatedData)
    return render_template('showOneshow.html', show=updatedshow,  user=User.get_by_id(data))

@app.route('/show/<int:id>/unlike', methods=['GET','PUT'])
def unlike_show(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'show_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    updatedshow = Show.getUsersWhoLiked(data)
    
    return render_template('showOneshow.html', show=updatedshow,  user=User.get_by_id(data))