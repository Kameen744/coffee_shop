import os
import re
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from backend.src.error_handler import ApiError

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# Raise errors


def raise_error(code=500):

    if code == 500:
        raise ApiError('Server Error', code)
    elif code == 410:
        raise ApiError('Resource Deleted', code)
    elif code == 404:
        raise ApiError('Not Found', code)
    elif code == 401:
        raise ApiError('Unauthorized Request', code)
    elif code == 403:
        raise ApiError('Forbidden Request', code)
    elif code == 422:
        raise ApiError('Unprocessable Request', code)

# Check resource and throw erorr if not found


def check_resource(resource, code):
    if not resource:
        raise_error(code)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/api/v1/drinks')
def get_drinks():
    # db_drop_and_create_all()
    drinks = [drink.short() for drink in Drink.query.all()]
    check_resource(drinks, 404)
    response_data = {'success': True, 'drinks': drinks}
    return jsonify(response_data)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/api/v1/drinks-detail')
def get_drink_details():

    drinks = [drink.long() for drink in Drink.query.all()]
    check_resource(drinks, 404)
    response_data = {'success': True, 'drinks': drinks}
    return jsonify(response_data)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/api/v1/drinks', methods=['POST'])
def add_drink():
    try:
        request_data = request.get_json()
        recipe = json.dumps(request_data['recipe'])

        new_drink = Drink(title=request_data['title'], recipe=recipe)
        Drink.insert(new_drink)
        new_drink = new_drink.long()
        return jsonify({'success': True, 'drinks': new_drink})
    except:
        raise_error(500)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/api/v1/drinks/<int:drink_id>')
def get_drink(drink_id):

    drink = Drink.query.get(drink_id)
    check_resource(drink, 404)
    Drink.update(drink)
    return jsonify({'success': True, 'drinks': drink.long()})


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/api/v1/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.get(drink_id)
    check_resource(drink, 410)
    Drink.delete(drink)
    return jsonify({'success': True, 'delete': drink.id})


    # Error Handling
'''
    Example error handling for unprocessable entity
'''


# @app.errorhandler(422)
# def unprocessable(error):
#     return jsonify({
#         "success": False,
#         "error": 422,
#         "message": "unprocessable"
#     }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
This Handles the errors through ApiError handler i implemented in prev. proj.
'''


@app.errorhandler(ApiError)
def handle_api_errors(error):
    return error.to_json()


'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
