from flask import Flask
from flask_cors import CORS
import logging
from routes.user_routes import create_user_routes
from routes.reimbursement_routes import create_reimbursement_routes

app: Flask = Flask(__name__)
CORS(app)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

create_user_routes(app)
create_reimbursement_routes(app)

# Start web server
app.run(debug=True)
