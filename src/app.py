from typing import Any

from flask import Flask, jsonify, request

from src.db import LocalDB
from src.logic import Logic
from src.user import User

app = Flask(__name__)
_db = LocalDB()
logic = Logic(_db)


@app.route('/user/<userId>', methods=['GET'])
def getUser(userId):
    try:
        user: User = logic.getUserById(userId)
        return jsonify(user.__dict__)
    except:
        return jsonify({'message': 'User not found'}), 404


@app.route('/user/<userId>', methods=['POST'])
def createUser(userId):
    if not (json := request.json) or not _checkInput(json):
        return jsonify({
            'message': 'Error in the request body',
        }), 400

    name: str = json.get('name')
    postalCode: str = json.get('postalCode')
    try:
        user: User = logic.createUserWithId(userId=userId, name=name, postalCode=postalCode)
        return jsonify(user.__dict__)
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/user/<userId>', methods=['PUT', 'PATCH'])
def updateUser(userId):
    if not (json := request.json) or not _checkInput(json):
        return jsonify({
            'message': 'Error in the request body',
        }), 400

    postalCode = json.get('postalCode')
    try:
        result = logic.updateUserById(userId, postalCode)
        return jsonify(result)
    except Exception as e:
        # Custom exceptions here would allow sending appropriate codes
        return jsonify({'message': str(e)}), 404


def _checkInput(json: Any | None) -> bool | None:
    json = request.json
    return json and json.get('name') and json.get('postalCode')


if __name__ == '__main__':
    app.run(debug=True)
