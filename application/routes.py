#!/usr/bin/python3

from application import app, db
from application.models import Owner, Business
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):
    ownername = StringField('Business Owner Name')
    businessname = StringField('Business Name')
    submit = SubmitField('Add Businesse')

class UpdateForm(FlaskForm):
    oldname = StringField('Current Business Name')
    ownername = StringField("Business Owner's Name")
    newname = StringField('New Business Name')
    submit = SubmitField('Save Changes')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view():
    fulllist = Business.query.with_entities(Business.name)
    return render_template('view.html', fulllist = fulllist) 

@app.route('/add', methods=['GET', 'POST'])
def add():
    error = ""
    form = AddForm()

    if request.method == 'POST':
        ownername = form.ownername.data
        businessname = form.businessname.data

        owner = Owner(name = ownername)
        db.session.add(owner)
        db.session.commit()
        business = Business(name = businessname, owner = Owner.query.filter_by(name=ownername).first())
        db.session.add(business)
        db.session.commit()

        if len(ownername) == 0 or len(businessname) == 0:
            error = "Please supply both your name and the business name"
        else:
            return 'You have now been added'

    return render_template('add.html', form=form, message=error)

@app.route('/update', methods=['GET', 'POST'])
def update():
    error = ""
    form = UpdateForm()

    if request.method == 'POST':
        oldname = form.oldname.data
        ownername = form.ownername.data
        newname = form.newname.data

        owner = Owner.query.filter_by(name=ownername).first()
        business = Business.query.filter_by(name=oldname).first()

        if business.owner_id == owner.id:
            business.name = newname
            db.session.commit()
            if newname == business.name:
                return "Your changes have now been saved"
        
        else:
            return "The details entered do not match our records"

    return render_template('update.html', form=form, message=error)


#@app.route('/update/<name>')
#def update(name):
#    first_game = Games.query.first()
#    first_game.name = name
#    db.session.commit()
#    return first_game.name

#@app.route('/delete')
#def delete():
#    delete_game = Games.query.first()
#    db.session.delete(delete_game)
#    db.session.commit()
#    return "Deleted gane"
