from flask.helpers import flash
from flask_restful import Resource, reqparse
from database import db
from models import *
from validation import *
from flask_security import Security, login_required,auth_required, SQLAlchemySessionUserDatastore
import json
from datetime import date, time, timedelta

class User_decks(Resource):
    @auth_required('token')
    def get(self, user_id):
        datas = db.session.query(cardecks).filter(cardecks.user_id==user_id).all()
        if datas:
            data_dict={}
            for data in datas:
                data_dict[data.deck_id]={
                    "topic": data.topic,
                    "last_review": data.last_r,
                    }
            #print(data_dict)
            return json.dumps(data_dict, sort_keys=True, default=str)
        else:
            return None, 404

    def put(self, user_id):
        deck_parser = reqparse.RequestParser()
        deck_parser.add_argument('topic')
        args = deck_parser.parse_args()
        deck_deets = {'deck_topic': args.get('topic', None)}
        if type(deck_deets['deck_topic'])==str:
            try:
                cardecks.query.filter_by(user_id=user_id).filter_by(topic=deck_deets['deck_topic']).update(dict(topic = deck_deets['deck_topic']))
                db.session.commit()
                return 'Successfully Updated'
            except:
                db.session.rollback()
        else:
            raise putd_error(status_code=400, error_code = "TOPIC100", error_message="Topic should be string.")

    def post(self, user_id):
        #parser
        deck_parser = reqparse.RequestParser()
        deck_parser.add_argument('topic')
        args = deck_parser.parse_args()
        deck_deets = {'topic': args.get('topic', None)}
        if type(deck_deets['topic'])==str:
            datal =cardecks.query.filter(cardecks.topic==deck_deets['topic']).first()
            if datal is None:
                try:
                    db.session.add(cardecks(topic = deck_deets['topic'], user_id=user_id))
                    db.session.commit()
                    return 'Deck Successfuly Created'
                except:
                    db.session.rollback()
            else:
                return 'Deck already exist', 409
        elif deck_deets['topic']==None:
            raise putd_error(status_code=400, error_code = "TOPIC100", error_message="Topic is required and should be string.")



class Deck(Resource):
    @login_required
    def get(self, user_id, deck_id):
        datal = db.session.query(flashcard).filter(flashcard.deck_id==deck_id).all()
        if datal:
            data_dict={}
            for data in datal:
                data_dict[data.card_id]={
                    "front": data.front,
                    "back": data.back,
                    "time": data.time,
                    "interval": data.interval
                    }
                print(data_dict)
            return json.dumps(data_dict, default=str)
        else:
            return None, 404

    def delete(self, user_id, deck_id):
        data = db.session.query(cardecks).filter(cardecks.user_id==user_id).first()
        if data==None:
            return "Decks not found", 404
        else:
            flashcard.query.filter(flashcard.deck_id==deck_id).delete()
            cardecks.query.filter(cardecks.deck_id==deck_id).delete()
            db.session.commit()
            return "Successfully Deleted"

    def post(self, user_id, deck_id):
        deck_parser = reqparse.RequestParser()
        deck_parser.add_argument('front')
        deck_parser.add_argument('back')
        args = deck_parser.parse_args()
        deck_deets = {'front': args.get('front', None), 'back':args.get('back', None)}
        #print("Enter 1", deck_deets)
        if type(deck_deets['front'])==str:
            #print("Enter 2")
            if type(deck_deets['back'])==str:
                #print("Enter 3")
                datal =flashcard.query.filter(flashcard.deck_id==deck_id).filter(flashcard.front==deck_deets['front']).first()
                if datal is None:
                    #print("Enter 4")
                    try:
                        db.session.add(flashcard(deck_deets['front'], deck_deets['back'], deck_id=deck_id))
                        db.session.commit()
                        #print("Enter 5")
                        return 'Successfully added Card', 201
                    except:
                        db.session.rollback()
                        #print("Enter 6")
                else:
                    #print("Enter 7")
                    return 'Card already exist', 409
            else:
                print("Enter 8")
                raise putd_error(status_code=400, error_code = "CARD102", error_message="Back Card should be string.")
        elif deck_deets['front']==None:
            print("Enter 9")
            raise putd_error(status_code=400, error_code = "CARD001", error_message="Front Card is required and should be string.")


class Cards(Resource):
    @login_required
    def get(self, user_id, deck_id, card_id):
        data = flashcard.query.filter(flashcard.card_id==card_id).first()
        if data:
            data_dict={
                "card_id": card_id,
                "front": data.front,
                "back": data.back,
                "interval": data.interval,
                "time": data.time
                }
            return json.dumps(data_dict, default=str)
        else:
            return None, 400
    def post(self,user_id, deck_id, card_id):
        data_parser = reqparse.RequestParser()
        data_parser.add_argument('diff')
        args = data_parser.parse_args()
        deck_deets = {'diff': args.get('diff', None)}
        datal =flashcard.query.filter(flashcard.card_id==card_id).first()
        today=date.today()
        interval = datal.interval
        diff=int(deck_deets['diff'])
        fudate = today + timedelta(days=interval+int(diff))
        new_interval = interval
        if diff == 1:
            new_interval+=1
        elif diff ==3:
            if interval > 1:
                new_interval-=1
        try:
            flashcard.query.filter_by(card_id=card_id).update(dict(time=fudate, interval=new_interval))
            cardecks.query.filter(cardecks.deck_id==deck_id).update(dict(last_r=today))
            db.session.commit()
            return "Successful"
        except Exception as e:
            db.session.rollback()
            print('Could not Update Card for 1\n', e)
            return "Nope"

    def put(self, user_id, deck_id, card_id):
        #parser
        deck_parser = reqparse.RequestParser()
        deck_parser.add_argument('front')
        deck_parser.add_argument('back')
        args = deck_parser.parse_args()
        deck_deets = {'front': args.get('front', None), 'back':args.get('back', None)}
        if type(deck_deets['front'])==str:
            if type(deck_deets['back'])==str:
                try:
                    flashcard.query.filter_by(card_id=card_id).update(dict(front = deck_deets['front'], back = deck_deets['back']))
                    
                    db.session.commit()
                    return 'Card Update Successfully'
                except:
                    db.session.rollback()
            else:
                raise puts_error(status_code=400, error_code = "CARD002", error_message="Back Card should be string.")
        elif deck_deets['front']==None:
            raise puts_error(status_code=400, error_code = "CARD001", error_message="Front Card is required and should be string.")


    def delete(self, user_id, deck_id, card_id):
        try:
            flashcard.query.filter(flashcard.card_id==card_id).delete()
            db.session.commit()
            return "Successfully Deleted"            
        except:
            return "Card Does not Exist"
