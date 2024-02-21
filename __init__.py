from flask import Flask,jsonify,Response,request
from db.db import db,configure_db
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from routes.user_routes import user_bp
from models.clientuser import ClientUser
from models.clientuser import OpsUser
from controllers.token_ import genrateToken,verify_
from controllers.upload import uploadfile,list_,move
from flask_mail import Mail,Message

# Initializing Flask instance
app = Flask(__name__)
api=Api(app)
configure_db(app)

#parser to validate user input while inserting data into tables
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("uname", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("email", type=str, help="Name of the user is required", required=True)
user_put_args.add_argument("password", type=str, help="Name of the user is required", required=True)

# parser to validate user input during login 
user_login_args = reqparse.RequestParser()
user_login_args.add_argument("uid", type=str, help="User Id is required", required=True)
user_login_args.add_argument("password", type=str, help="Name of the user is required", required=True)


# user to create data display decorator
resource_fields = {
	'id': fields.String,
	'uname': fields.String,
	'email': fields.String,
	'password': fields.String,
	"verified":fields.Integer
}

# Function to send mail for verification
def sendMail(email,token):
	app.config["MAIL_SERVER"]="smtp.gmail.com"
	app.config["MAIL_PORT"]=465
	app.config["MAIL_USERNAME"]="trueboy978@gmail.com"
	app.config["MAIL_PASSWORD"]="yhsfarvllnhgwrjn"
	app.config["MAIL_USE_TLS"]=False
	app.config["MAIL_USE_SSL"]=True
	mail=Mail(app)
	msg = Message( 
					'VERIFY', 
					sender ="abc@gmail.com", 
					recipients = [email] 
				) 
	msg.body = f"Click the link to verify your email ..\nhttp://127.0.0.1:5000/verify/{token}"
	mail.send(msg) 
	return f'Email send to {email}'


# APIs for userclient login and deletion of all client (if nedded)
class userclient(Resource):
	def get(self):
		args = user_login_args.parse_args()
		result = ClientUser.query.filter_by(id=args["uid"]).first()
		if not result:
			abort(404, message="Could not find user with that id")
		elif(result.verified==1):
			if(result.password==args["password"]):
				return jsonify({"To list files use :":f"http://127.0.0.1:5000/user/{args['uid']}","To download files :":"http://127.0.0.1:5000/user/download/<filename>"})
			else:
				return "Incorrect Password.."
		else:
			return "Please verify your email.."
		
	# Delete all UserClients if necessary
	def delete(self, user_id):
		try:
			ClientUser.query.delete()
			db.session.commit()
			db.session.commit()
			return 'Data deleted successfully..', 204
		except Exception as e:
			return f"Error_occured :{e} .."
	
# API it controls user client Signup and display information of userclient
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
		if not result:
			abort(404, message="No user available..")
		return result
	
# Apis  of opsuser to login use req("GET") and Signup use req("POST")
class opsclient(Resource):
	def get(self):
		args = user_login_args.parse_args()
		result = OpsUser.query.filter_by(id=args["uid"]).first()
		if not result:
			abort(404, message="Invalid ops user ..")
		elif(result.password==args["password"]):
			return jsonify({"To upload a file :": f"http://127.0.0.1:5000/opsuser/upload/{args['uid']}","Note :":"Add file in form body with name 'file' to identify it"})
		else:
			abort(message="Incorrect Password..")
	def post(self):
		try:
			args=user_put_args.parse_args()	
			opuser=OpsUser(uname=args['uname'], email=args['email'], password=args['password'])
			db.session.add(opuser)
			db.session.commit()
			print(opuser)
			return f"Ops user created successfully..Please login : http://127.0.0.1:5000/opsuser ['GET'] with uid and password"
		except Exception as e:
			return f"Error_occured : {e}"

# api for user signup
api.add_resource(SignUp, "/signup")
# api for user login
api.add_resource(userclient, "/userlogin")
# api for opsuser login
api.add_resource(opsclient, "/opsuser")

#Common health check 
@app.route('/')
def health():
    return 'Server is Working Fine....'


# For demo purpose to delete all data only for developer use
@app.route("/deleteall",methods=["DELETE"])
def delete():
	print("Deleted..")
	ClientUser.query.delete()
	db.session.commit()
	return 'All data was removed..', 204

# verify the link send to email
@app.route("/verify/<token>",methods=["GET"])
def valid(token):
	try:
		data=verify_(token)
		user =ClientUser.query.get(data["user"])
		user.verified=1
		db.session.commit()
		print("User Data :",user)
		return "Email Verified..",204
	except Exception as e:
		return f"Error_occured : {e}"

# Upload file only for opsuser
@app.route("/opsuser/upload/<id>",methods=["POST"])
def upload(id):
	result = OpsUser.query.filter_by(id=id).first()
	if not result:
		abort(404, message="Invalid ops user ..")
	else:
		return uploadfile(request.files["file"],id)
	
@app.route("/userlogin/listall/<id>",methods=["GET"])		
def listall(id):
		try:
			result = ClientUser.query.filter_by(id=id).first()
			if not result:
				return "Could not find user with that id .."
			else:
				res="Files Available to download :\n"+list_()+f"\nTo Download file :http://127.0.0.1:5000/userlogin/{id}/<filename>"
				return res
		except Exception as e:
			return f"Error_occured : {e}"

# Download api for clientuser
@app.route("/userlogin/<id>/<filename>",methods=["GET"])		
def download_link(id,filename):
		try:
			result = ClientUser.query.filter_by(id=id).first()
			if not result:
				return "Could not find user with that id .."
			else:
				token=genrateToken(id)
				return jsonify({"Download-link ":f"http://127.0.0.1:5000/download/{filename}/{token}","Note":"To download file add BearerToken : {token} in Autherization header"})
		except Exception as e:
			return f"Error_occured : {e}"
		
# secure route to download file
@app.route("/dowload/<filename>/<token>",methods=["GET"])	
def download(filename,token):
	try:
		data_api=verify_(token)
		data_auth=verify_(request.args.get("token"))
		if (data_api["user"]==data_auth["user"]):
			move(filename)
		else:
			return "Invalid token.."
	except Exception as e:
		return f"Error_occured : {e}"

if __name__ == "__main__":
	app.run(debug=True)
