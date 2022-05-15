from flask import Flask, render_template, request, redirect
from datetime import datetime
import pymongo
from bson.objectid import ObjectId
#from redis import Redis

app = Flask(__name__)
#redis = Redis(host='redis', port=6379)


################## connecting database (mongodb)

client = pymongo.MongoClient(host='db_mongo',port=27017,username='root',password='pass',authSource='admin')
db = client.get_database('user')

##################  using mongo atlas

#CONNECTION_STRING = 'mongodb+srv://db:db123@cluster0.j523m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#client = pymongo.MongoClient(CONNECTION_STRING)
#db = client.get_database('user')

##################   localhost

#CONNECTION_STRING = 'mongodb://localhost:27017/''
#client = pymongo.MongoClient(CONNECTION_STRING)
#db = client.get_database('user')



user_collection = pymongo.collection.Collection(db, 'user')

group_collection = pymongo.collection.Collection(db, 'group')


@app.route('/')
@app.route('/admin', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        datetime_now = datetime.now()
        user_collection.insert_one({'name' : name, 'date' : datetime_now})
        return redirect('/admin')
    else:
        return render_template('index.html',users = user_collection.find())





@app.route('/admin/delete/<_id>')
def delete(_id):
    try:
        print(id)
        user_collection.delete_one({'_id': ObjectId(_id)})
        return redirect('/admin')
      
    except:
        return"There was an issue deleteing existing user"


@app.route('/admin/update/<_id>', methods=['POST', 'GET'])
def update(_id):
    if request.method == 'POST':
        new_name = request.form['name']
        print(new_name)
        print(_id)
        try:
            user_collection.find_one_and_update({"_id": ObjectId(_id)}, 
                                 {"$set": {"name": new_name}})
            return redirect('/admin')

        except:
            return"There was an issue updating existing user"
        
    else:
        return render_template('update.html', _id = _id)


######### group code






@app.route('/group', methods=['POST', 'GET'])
def group():
    if request.method == 'POST':
        groupname = request.form['groupname']
        print(groupname)
        group_collection.insert_one({'groupname' : groupname})
        return redirect('/group')
    else:
        #return group_collection.find()
        return render_template('group.html',users = group_collection.find())


@app.route('/group/delete/<_id>')
def groupdelete(_id):
    try:
        print(id)
        group_collection.delete_one({'_id': ObjectId(_id)})
        return redirect('/group')
      
    except:
        return"There was an issue deleteing existing user"




@app.route('/group/update/<_id>', methods=['POST', 'GET'])
def groupupdate(_id):
    if request.method == 'POST':
        new_groupname = request.form['groupname']
        print(new_groupname)
        print(_id)
        try:
            group_collection.find_one_and_update({"_id": ObjectId(_id)}, 
                                 {"$set": {"groupname": new_groupname}})
            return redirect('/group')

        except:
            return"There was an issue updating existing user"
        
    else:
        return render_template('groupupdate.html', _id = _id)





@app.route('/group/add/member/<_id>', methods=['POST', 'GET'])
def groupmember(_id):
    if request.method == 'POST':
        user_id = request.form['id']
        print(user_id)
        print(_id)
        try:
            user_collection.find_one_and_update({"_id": ObjectId(user_id)}, 
                                 {"$set": {"groupid": _id}})
            return redirect('/group/add/member/'+_id)


        except:
            return"There was an issue updating existing user"
    else:
        return render_template('groupmember.html', users = user_collection.find(), id = _id)





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=5001)
    