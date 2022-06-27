from flask import Flask, request, render_template, redirect, url_for
from flask import current_app as app
from flask.helpers import flash
from models import *
from tasks import just_say_hello
from nails import send_email
from flask_security import login_required
from flask_login import current_user
from datetime import date, time, timedelta
import json
from main import cache



@app.route("/", methods=["GET"])
#@cache.cached(timeout=50)
def log():
    if request.method == 'GET':
        if current_user:
            try:
                redirect_dash = current_user.id
                return redirect('/dashboard/{}'.format(redirect_dash))
            except:
                pass
        return render_template('index2.html')


@app.route("/dashboard/<int:user_id>/", methods=["GET","POST"])
@login_required
def dash(user_id):
    if request.method == 'GET':
        email = db.session.query(User).filter(User.id==user_id).first().email
        #(flenv2) F:\Projects\IITM\MAD2\ARework>celery -A main.celery beat --max-interval 1 -l info
        job=send_email(to_address=email, subject="Reminder", message="Review Flashcards everyday for good memory")
        return render_template('newdash.html', cu=user_id)
#        tack = db.session.query(cardecks).filter(cardecks.user_id==user_id).order_by(cardecks.last_r).all()
#        inter = db.session.query(cardecks.topic, db.func.avg(flashcard.interval).label('avg'), db.func.max(flashcard.interval).label('max'), db.func.count(flashcard.card_id).label('count')).filter(cardecks.user_id==user_id).filter(flashcard.deck_id==cardecks.deck_id).group_by(flashcard.deck_id).all()
#        score=[]
#        for i in inter:
#            score_deck = (int(i.avg)*100)/(i.max)
#            score.append("{:.2f}".format(score_deck))
#        lent = len(tack)
#        return render_template('dash.html', stack=tack, lent=lent, user_id=user_id, score=score)


#####################################################################################################
#################################DECK Creation and Deletion##########################################
####################################################################################################3
@app.route("/<int:user_id>/create_deck", methods=["GET","POST"])
@login_required
def add_deck(user_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    if request.method=='GET':
        return render_template('add.html', user_id=user_id)
    elif request.method=='POST':
        topic = request.form['topic']
        datal =cardecks.query.filter(cardecks.topic==topic).filter(cardecks.user_id==user_id).first()
        if datal is None:
            try:
                db.session.add(cardecks(topic = topic, user_id=user_id))
                db.session.commit()
                return redirect("/dashboard/{}".format(user_id))
            except:
                db.session.rollback()
        else:
            flash("Topic Already Exists")
            return render_template('add.html',user_id=user_id)

        return redirect("/dashboard/{}".format(user_id))

@app.route("/<int:user_id>/<int:deck_id>/delete", methods=["GET"])
@login_required
def del_deck(user_id, deck_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    elif current_user.id==user_id:
        flashcard.query.filter(flashcard.deck_id==deck_id).delete()
        cardecks.query.filter(cardecks.deck_id==deck_id).delete()
        db.session.commit()
        return redirect("/dashboard/{}".format(user_id))

@app.route('/<int:user_id>/<int:deck_id>',methods=["GET"])
@login_required
def deck_page(user_id, deck_id):
    deck = flashcard.query.filter(flashcard.deck_id==deck_id).all()
    lent=len(deck)
    return render_template('decks.html', deck=deck, lent=lent, user_id=user_id, deck_id=deck_id)

#####################################################################################################
##########################Flash Card Creation, Updation and Deletion#################################
####################################################################################################3
@app.route("/<int:user_id>/<int:deck_id>/create_card", methods=["GET","POST"])
@login_required
def add_cards(user_id, deck_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    if request.method=='GET':
        return render_template('addcards.html', user_id=user_id, deck_id=deck_id)
    elif request.method=='POST':
        front=request.form['front']
        back=request.form['back']
        datal =flashcard.query.filter(flashcard.deck_id==deck_id).filter(flashcard.front==front).first()
        if datal is None:
            try:
                db.session.add(flashcard(front = front,back = back, deck_id=deck_id))
                db.session.commit()
            except:
                db.session.rollback()
        else:
            flash("Card Already Exists")
            return render_template('addcards.html',user_id=user_id, deck_id=deck_id)

        return redirect("/{}/{}".format(user_id,deck_id))

@app.route("/<int:user_id>/<int:deck_id>/<int:card_id>/update", methods=["GET","POST"])
@login_required
def update_cards(user_id, deck_id,card_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    if request.method=='GET':
        card =flashcard.query.filter(flashcard.card_id==card_id).first()
        return render_template('upcards.html', user_id=user_id, deck_id=deck_id, card_id=card_id, card=card)
    elif request.method=='POST':
        card =flashcard.query.filter(flashcard.card_id==card_id).first()
        front=request.form['front']
        back=request.form['back']
        datal =flashcard.query.filter(flashcard.deck_id==deck_id).filter(flashcard.front==front, flashcard.back==back).first()
        if datal is None:
            try:
                flashcard.query.filter_by(card_id=card_id).update(dict(front=front, back=back))
                db.session.commit()
            except:
                db.session.rollback()
        else:
            flash("Change was not made")
            return render_template('upcards.html', user_id=user_id, deck_id=deck_id, card_id=card_id, card=card)

        return redirect("/{}/{}".format(user_id,deck_id))


@app.route("/<int:user_id>/<int:deck_id>/<int:card_id>/delete", methods=["GET"])       
def del_cards(user_id, deck_id, card_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    flashcard.query.filter(flashcard.card_id==card_id).delete()
    db.session.commit()
    return redirect("/{}/{}".format(user_id, deck_id))
#####################################################################################################
##########################Space Repretition OR Reviewing Cards#######################################
####################################################################################################3
@app.route("/<int:user_id>/<int:deck_id>/review", methods=["GET","POST"])
@login_required
def review(user_id, deck_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    if request.method=='GET':
        cards = flashcard.query.filter(flashcard.deck_id==deck_id).all()
        lent=len(cards)
        return render_template('review.html', user_id=user_id, deck_id=deck_id, cards=cards, lent=lent)
    elif request.method=='POST':
        cards = flashcard.query.filter(flashcard.deck_id==deck_id).all()
        for i in range(1, len(cards)+1):
            diff = request.form['diff'+str(i)]
            card_id=request.form['card_id'+str(i)]
            if int(diff)==1:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    if interval==1:
                        flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate))
                    else:
                        flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate, interval=interval-1))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 1\n', e)
            elif int(diff)==2:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 2\n', e)
            else:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate, interval=interval+2))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 3\n', e)
    
    cardecks.query.filter_by(deck_id=deck_id).update(dict(last_r=date.today()))
    return redirect("/dashboard/{}".format(user_id))

#####################################################################################################
######################################New Review#####################################################
#####################################################################################################
@app.route("/<int:user_id>/<int:deck_id>/review2", methods=["GET","POST"])
@login_required
def review2(user_id, deck_id):
    if current_user.id !=user_id:
        return redirect('/dashboard/{}'.format(current_user.id))
    if request.method=='GET':
        cards = flashcard.query.filter(flashcard.deck_id==deck_id).all()
        lent=len(cards)
        return render_template('review2.html', user_id=user_id, deck_id=deck_id, cards=cards, lent=lent)
    elif request.method=='POST':
        cards = flashcard.query.filter(flashcard.deck_id==deck_id).all()
        for i in range(1, len(cards)+1):
            diff = request.form['diff'+str(i)]
            card_id=request.form['card_id'+str(i)]
            if int(diff)==1:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    if interval==1:
                        flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate))
                    else:
                        flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate, interval=interval-1))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 1\n', e)
            elif int(diff)==2:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 2\n', e)
            else:
                try:
                    today=date.today()
                    interval = flashcard.query.filter_by(card_id=card_id).first().interval
                    fudate = today + timedelta(days=interval+int(diff))
                    flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate, interval=interval+2))
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print('Could not Update Card for 3\n', e)
    
    cardecks.query.filter_by(deck_id=deck_id).update(dict(last_r=date.today()))
    return redirect("/dashboard/{}".format(user_id))

#####################################################################################################
##########################Celery Tasks#######################################
####################################################################################################3
#(flenv2) F:\Projects\IITM\MAD2\ARework>celery -A main.celery worker -l info
@app.route("/tasks/<user_id>", methods=['GET','POST'])
def tasks(user_id):
    job=just_say_hello.delay(user_id)
    return str(job), 200