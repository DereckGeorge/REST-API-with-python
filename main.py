from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

cars = {"BMW":{"type":"automatic","fuel":"diesel"},
        "RANGEROVER":{"type":"manual","fuel":"petrol"}}

class HellowWorld(Resource):
    def get(self,name):
        return cars[name]
    
    
api.add_resource(HellowWorld,"/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)