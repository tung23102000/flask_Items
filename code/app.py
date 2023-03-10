from ast import Delete
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required


from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'mtp'
api = Api(app)

jwt = JWT(app,authenticate,identity) #/auth

items=[
    
]
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank")
       
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name']==name, items), None)
        
        return {'item': item}, 200 if item else 404 #trả về 200 nếu item not None còn ko là 404
        
    def post(self, name):
      
        data= Item.parser.parse_args()
        
        if next(filter(lambda x: x['name']==name, items), None):
            return {"message": f"An item with name '{name}' already exists"},400
        # data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item,201
    
    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message': "Item delete"}
    
    def put(self, name):
       
        # data = request.get_json()
        data= Item.parser.parse_args()
        item = next(filter(lambda x: x['name']==name,items), None)
        # nếu ko thấy thì tạo mới còn ko thì sẽ cập nhật lại item đó
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else: 
            item.update(data)
        return item
            
    
class ItemList(Resource):
    def get(self):
        return {'items':	items}
api.add_resource(Item, '/item/<string:name>')     #http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
