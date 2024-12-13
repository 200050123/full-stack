from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None

@app.route('/api/data/<client_id>', methods=['POST'])
@auth.login_required
def process_data(client_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use DD-MM-YYYY.'}), 422

    try:
        data = request.get_json()
        date_str = data['date']
        amount = data['amount']

        date = datetime.strptime(date_str, '%d-%m-%Y')

        print(f"Received data for client {client_id}: date={date}, amount={amount}")

        return jsonify({'message': 'Data processed successfully'}), 200
    except KeyError:
        return jsonify({'error': 'Missing required fields: date and amount'}), 422
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use DD-MM-YYYY.'}), 422

if __name__ == '__main__':
    app.run(debug=True)