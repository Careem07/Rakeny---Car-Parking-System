import datetime
import jwt
import pymysql as db
from flask import Flask, jsonify, request

# Run ipconfig in command prompt to get IP Address
IP_ADDRESS = '192.168.1.14'

app = Flask(__name__)

def Authenticate(encoded_token):
    decoded_token = jwt.decode(encoded_token, "nardine", algorithms=["HS256"])
    print(decoded_token)
    name = decoded_token['name']
    password = decoded_token['password']
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    query = 'SELECT userid FROM user WHERE name = \'' + \
        name + '\' AND pass = \'' + password + '\';'
    sel = cursor.execute(query)
    database_result = cursor.fetchall()
    if(database_result):
        return database_result[0][0]
    else:
        return -1


@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    slotID = data['slotID']
    startTime = data['startTime']
    print(startTime)
    print(slotID)
    print(userid)
    connection = db.connect(host='localhost', user='root', passwd='',
                                database='park_db')
    cursor = connection.cursor()
    query = 'DELETE FROM parkreserve WHERE'
    query = query + ' slotid = \'' + slotID +'\''
    query = query + ' AND userid = \'' + str(userid) + '\''
    query = query + ' AND starttime = \'' + startTime + '\''
    print(query)
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()   
    query = 'UPDATE `garage` SET `free`= 1 WHERE id=' + slotID
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()
    return 'Success'

@app.route('/test', methods=['POST'])
def test():
    return 'test'


@app.route('/login', methods=['POST'])
def Login():
    data = request.json
    name = data['name']
    password = data['password']
    print('Name = ', name)
    # To be changed from computer to computer
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    query = 'SELECT * FROM user WHERE name = \'' + \
        name + '\' AND pass = \'' + password + '\';'
    sel = cursor.execute(query)
    database_result = cursor.fetchall()
    response = dict()
    if(database_result):
        response['success'] = True

        encoded_jwt = jwt.encode(
            {"name": name, "password": password}, "nardine", algorithm="HS256")

        response['token'] = encoded_jwt
    else:
        response['success'] = False

        response['token'] = ''
    return jsonify(response)


@app.route('/signup', methods=['POST'])
def SignUp():
    data = request.json
    name = data['name']
    password = data['password']
    email = data['email']
    carlic = data['carlic']
    brand = data['brand']
    colour = data['colour']
    mobile = data['mobile']
    nationalid = data['nationalid']
    gender = data['gender']

    response = dict()

    # To be changed from computer to computer
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()

    # Check if name is unique
    name_query = "SELECT * FROM user WHERE name = \'" + name + '\';'
    sel = cursor.execute(name_query)
    name_database_result = cursor.fetchall()

    if(name_database_result):
        response['success'] = False
        response['not_unique'] = 'name'
        response['token'] = ''
        return jsonify(response)

    # Check if email is unique
    email_query = "SELECT * FROM user WHERE email = \'" + email + '\';'
    sel = cursor.execute(email_query)
    email_database_result = cursor.fetchall()

    if(email_database_result):
        response['success'] = False
        response['not_unique'] = 'email'
        response['token'] = ''
        return jsonify(response)

    query = 'INSERT INTO `user`(`name`, `email`, `pass`, `phone`, `carlic`, `brand`, `colour`, `nationalid`, `gender` )'
    query = query + ' VALUES ('
    query = query + '\'' + name + '\', '
    query = query + '\'' + email + '\', '
    query = query + '\'' + password + '\', '
    query = query + '\'' + mobile + '\', '
    query = query + '\'' + carlic + '\', '
    query = query + '\'' + brand + '\', '
    query = query + '\'' + colour + '\', '
    query = query + '\'' + nationalid + '\','
    query = query + '\'' + gender + '\')'
    print(query)
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()

    response['success'] = True

    encoded_jwt = jwt.encode(
        {"name": name, "password": password}, "nardine", algorithm="HS256")
    response['token'] = encoded_jwt
    response['not_unique'] = ''
    return response


@app.route('/parking1_init', methods=['GET'])
def parking1_init():
    query = 'Select free From garage where id >= 20 AND id <= 34'

    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()

    response = dict()
    response['parking'] = []
    reserve = []
    for i in range(0, len(database_result)):
        if(database_result[i][0] == 0):
            reserve.append(True)
        else:
            reserve.append(False)
    response['parking'] = reserve
    return response


@app.route('/parking2_init', methods=['GET'])
def parking2_init():
    query = 'Select free From garage where id >= 8 AND id <= 19'

    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()

    response = dict()
    response['parking'] = []
    reserve = []

    for i in range(0, len(database_result)):
        if(database_result[i][0] == 0):
            reserve.append(True)
        else:
            reserve.append(False)
    response['parking'] = reserve
    return response


@app.route('/parking3_init', methods=['GET'])
def parking3_init():
    query = 'Select free From garage where id >= 1 AND id <= 7'

    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()

    response = dict()
    response['parking'] = []
    reserve = []
    for i in range(0, len(database_result)):
        if(database_result[i][0] == 0):
            reserve.append(True)
        else:
            reserve.append(False)
    response['parking'] = reserve
    return response


@app.route('/book', methods=['POST'])
def book():
    data = request.json
    index = data['index']
    startDate = data['startDate']
    endDate = data['endDate']
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    if(userid != -1):
        print(userid)

        connection = db.connect(host='localhost', user='root', passwd='',
                                database='park_db')
        cursor = connection.cursor()
        query = 'INSERT INTO `parkreserve`( `starttime`, `endtime`, `userid`, `slotid`)'
        query = query + ' VALUES ('
        query = query + '\'' + startDate + '\', '
        query = query + '\'' + endDate + '\', '
        query = query + '\'' + str(userid) + '\', '
        query = query + '\'' + str(index) + '\')'
        sel = cursor.execute(query)
        connection.commit()
        database_result = cursor.fetchall()
        query = 'UPDATE `garage` SET `free`= 0 WHERE id=' + str(index)
        sel = cursor.execute(query)
        connection.commit()
        database_result = cursor.fetchall()
    return "Success"


@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    query = 'SELECT email, gender, phone, carlic, brand, colour FROM user WHERE userid = \'' + str(userid) + '\''
    connection = db.connect(host='localhost', user='root',
                            passwd='', database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()
    response = dict()
    response['email'] = database_result[0][0]
    response['gender'] = database_result[0][1]
    response['phone'] = database_result[0][2]
    response['carLicense'] = database_result[0][3]
    response['carBrand'] = database_result[0][4]
    response['carColour'] = database_result[0][5]
    return jsonify(response)


@app.route('/current_bookings', methods=['POST'])
def current_bookings():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    query = 'SELECT starttime, endtime, slotid FROM parkreserve WHERE userid = \'' + \
        str(userid) + '\''
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()
    bookings = []
    for i in range(0, len(database_result)):
        
        now = datetime.datetime.now()
        if(database_result[i][1] > now):
            start = str(database_result[i][0])
            start = start[0:len(start)-3]
            end = str(database_result[i][1])
            end = end[0:len(end)-3]
            slotID = str(database_result[i][2])
            tempArr = []
            tempArr.append(start)
            tempArr.append(end)
            tempArr.append(slotID)
            bookings.append(tempArr)
    response = dict()
    response['bookings'] = bookings
    return jsonify(response)


@app.route('/booking_history', methods=['POST'])
def bookings_history():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    query = 'SELECT starttime, endtime FROM parkreserve WHERE userid = \'' + \
        str(userid) + '\''
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    sel = cursor.execute(query)
    database_result = cursor.fetchall()
    bookings = []
    for i in range(0, len(database_result)):
        
        now = datetime.datetime.now()
        if(database_result[i][1] <= now):
            start = str(database_result[i][0])
            start = start[0:len(start)-3]
            end = str(database_result[i][1])
            end = end[0:len(end)-3]
            tempArr = []
            tempArr.append(start)
            tempArr.append(end)
            bookings.append(tempArr)
    response = dict()
    response['bookings'] = bookings
    return jsonify(response)

@app.route('/change_username', methods = ['POST'])
def change_username():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    newName = data['newName']
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()

    # Check if name is unique
    name_query = "SELECT * FROM user WHERE name = \'" + newName + '\';'
    sel = cursor.execute(name_query)
    name_database_result = cursor.fetchall()
    response = dict()
    if(name_database_result):
        response['success'] = False
        return jsonify(response)
    query = 'UPDATE user SET name = \'' + newName + '\' WHERE userid = \'' + str(userid) + '\''
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()
    response['success'] = True
    return jsonify(response)

@app.route('/change_password', methods = ['POST'])
def change_password():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    newPassword = data['newPassword']
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    response = dict()
    query = 'UPDATE user SET pass = \'' + newPassword + '\' WHERE userid = \'' + str(userid) + '\''
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()
    response['success'] = True
    return jsonify(response)



@app.route('/change_car_details', methods = ['POST'])
def change_car_details():
    data = request.json
    encoded_token = data['token']
    userid = Authenticate(encoded_token)
    newCarLicence = data['newCarLicence']
    newCarBrand = data['newCarBrand']
    newCarColour = data['newCarColour']
    connection = db.connect(host='localhost', user='root', passwd='',
                            database='park_db')
    cursor = connection.cursor()
    response = dict()
    query = 'UPDATE user SET'
    quert = query + ' carlic = \'' + newCarLicence + '\','
    query = query + ' brand = \'' + newCarBrand + '\','
    query = query + ' colour = \'' + newCarColour + '\''
    query = query + 'WHERE userid = \'' + str(userid) + '\''
    sel = cursor.execute(query)
    connection.commit()
    database_result = cursor.fetchall()
    response['success'] = True
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug = True, host = IP_ADDRESS)