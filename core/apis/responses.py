from flask import Response, jsonify, make_response

class APIResponse:
    @staticmethod
    def respond(data=None, message=None, status_code=200):
        response = {
            'status': 'success',
            'data': data,
            'message': message
        }
        return jsonify(response), status_code

    @staticmethod
    def respond_error(message=None, status_code=400):
        response = {
            'status': 'error',
            'message': message,
        }
        return jsonify(response), status_code

    @staticmethod
    def respond_error_with_details(message=None, status_code=400, error=None):
        response = {
            'status': 'error',
            'message': message,
            'error': error
        }
        return jsonify(response), status_code    

