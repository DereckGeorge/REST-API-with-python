from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

#data store for API keys 
api_keys = {
    'api_key1': {'user_id': 1},
    'api_key2': {'user_id': 2}
}

# Request parser for API key
api_key_parser = reqparse.RequestParser()
api_key_parser.add_argument('API-Key', type=str, required=True, location='headers', help='API key is required')

# Middleware to authenticate API key
def authenticate_api_key(api_key):
    if api_key in api_keys:
        return api_keys[api_key]
    else:
        abort(401, message='Invalid API key')

# Protected resource
class ProtectedResource(Resource):
    def get(self):
        args = api_key_parser.parse_args()
        api_key = args['API-Key']
        user_data = authenticate_api_key(api_key)
        return {'message': f'Protected endpoint accessed by user {user_data["user_id"]}'}

# Register resource
api.add_resource(ProtectedResource, '/protected')

if __name__ == '__main__':
    app.run(debug=True)
