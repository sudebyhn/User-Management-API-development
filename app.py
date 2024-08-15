from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'age': user.age
                })
            return {'message': 'User not found'}, 404
        else:
            users = User.query.all()
            return jsonify([{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'age': user.age
            } for user in users])

    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'], age=data['age'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully', 'user_id': new_user.id}, 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        user.age = data['age']
        db.session.commit()
        return {'message': 'User updated successfully'}

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

api.add_resource(UserResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='127.0.0.1', port=5000, debug=True)
