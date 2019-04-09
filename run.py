from flask import Flask
from flask import request

my_awesome_app = Flask(__name__)


@my_awesome_app.route('/')
def hello_world():
    return 'Hello World!'

@my_awesome_app.route('/api/diabetes', methods=['POST'])
def diabetes_api():
	req_data = request.get_json()

	key = req_data["key"]

	return key

if __name__ == '__main__':
    my_awesome_app.run()
