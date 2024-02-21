from flask import Flask,jsonify
from db.db import db,configure_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from routes.user_routes import user_bp
from models.clientuser import ClientUser
from models.clientuser import OpsUser
from .controllers.token_ import genrateToken
from flask_mail import Mail,Message


app = Flask(__name__)
api=Api(app)
configure_db(app)




# Use the configure_db function to set up the database
# db=configure_db(app)


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("uname", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("email", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("password", type=str, help="Name of the user is required", required=True)


user_login_args = reqparse.RequestParser()
user_login_args.add_argument("uid", type=str, help="User Id is required", required=True)
user_login_args.add_argument("password", type=str, help="Name of the user is required", required=True)



resource_fields = {
	'id': fields.String,
	'uname': fields.String,
	'email': fields.String,
	'password': fields.String
}


def sendMail(email,token):
	app.config["MAIL_SERVER"]="smtp.gmail.com"
	app.config["MAIL_PORT"]=465
	app.config["MAIL_USERNAME"]="trueboy978@gmail.com"
	app.config["MAIL_PASSWORD"]="yhsfarvllnhgwrjn"
	app.config["MAIL_USE_TLS"]=False
	app.config["MAIL_USE_SSL"]=True
	mail=Mail(app)
 
	msg = Message( 
					'Hello', 
					sender ="abc@gmail.com", 
					recipients = [email] 
				) 
	msg.body = f"Click the link to verify your email ..\nhttp://127.0.0.1:5000/verify/{token}"
	mail.send(msg) 
	return 'Sent'

@app.route('/')
def health():
    return 'Server is Working Fine....'

class userclient(Resource):
	@marshal_with(resource_fields)
	def get(self):
		args = user_login_args.parse_args()
		result = ClientUser.query.filter_by(id=args["uid"]).first()
		if not result:
			abort(404, message="Could not find user with that id")
		elif(result.password==args["password"]):
			return result
		else:
			return "Incorrect Password.."

	# @marshal_with(resource_fields)
	# def post(self, user_id):
	# 	args = user_put_args.parse_args()
	# 	result = ClientUser.query.filter_by(id=user_id).first()
	# 	if result:
	# 		abort(409, message="user id taken...")
			
	# 	user = ClientUser(id=user_id, uname=args['name'], views=args['views'], likes=args['likes'])
	# 	db.session.add(user)
	# 	db.session.commit()
	# 	return user, 201

	# @marshal_with(resource_fields)
	# def patch(self, user_id):
	# 	args = user_update_args.parse_args()
	# 	result = ClientUser.query.filter_by(id=user_id).first()
	# 	if not result:
	# 		abort(404, message="user doesn't exist, cannot update")

	# 	if args['name']:
	# 		result.name = args['name']
	# 	if args['views']:
	# 		result.views = args['views']
	# 	if args['likes']:
	# 		result.likes = args['likes']

	# 	db.session.commit()

	# 	return result

	def delete(self, user_id):
		try:
			ClientUser.query.delete()
			db.session.commit()
			db.session.commit()
			return 'Data deleted successfully..', 204
		except Exception as e:
			return f"Error_occured :{e} .."
	

class SignUp(Resource):
	def post(self):
		try:

			args=user_put_args.parse_args()	
			user=ClientUser(uname=args['uname'], email=args['email'], password=args['password'])
			db.session.add(user)
			db.session.commit()
			token=genrateToken(user.id)
			sendMail(user.email,token)
			return f"Data saved please verify your email {args['email']}..",200
		
		except Exception as e:
			return f"Error_occured :{e} .."

	@marshal_with(resource_fields)
	def get(self):
		result = ClientUser.query.all()
		for i in result:
			print(i.verified)
		if not result:
			abort(404, message="No user available..")
		return result

# For demo purpose to delete all data only for developer use
@app.route("/deleteall",methods=["DELETE"])
def delete():
	print("Deleted..")
	ClientUser.query.delete()
	db.session.commit()
	return 'All data was removed..', 204

# api for user signup
api.add_resource(SignUp, "/signup")
# api for user login
api.add_resource(userclient, "/userlogin")

if __name__ == "__main__":
	app.run(debug=True)

# app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)