from flask import Flask, render_template, request, jsonify, abort
from flask_mysqldb import MySQL
import mysql.connector
from flask_mysqlpool import MySQLPool
import json
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_POOL_NAME'] = 'mysql_pool'
app.config['MYSQL_POOL_SIZE'] = 30
mysql1 = MySQL(app)
#db = MySQLPool(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        AcctNum= request.form['Account_Number']
        OrderTimestamp= request.form['Order_Timestamp']
        ItemName= request.form['item_name']
        ItemQty= request.form['item_qty']
        ItemPrice = request.form['item_price']
        cur = mysql1.connection.cursor()

        cur.execute("INSERT INTO order_details(acct_number,order_timestamp,item_name,item_quantity,item_price) VALUES (%s,%s,%s,%s,%s)",(AcctNum, OrderTimestamp, ItemName, ItemQty,ItemPrice))
        
        mysql1.connection.commit()

        resultValue = cur.execute("SELECT distinct(acct_number) FROM order_details")
        if resultValue > 0:
        
            result_list = cur.fetchall() 
            fields_list = cur.description   # sql key name

        cur.close()
        #    mysql1.connection.close()
        #cur.close()
        column_list = []
        for i in fields_list:
           column_list.append(i[0])
        jsonData_list = []
        for row in result_list:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
        
                jsonData_list.append(data_dict)
        return jsonify({'Data': result_list})
        cur.close()
        
        #return 'success'
    return render_template('index.html')

@app.route('/top3price', methods=['GET', 'POST'])
def top3price():
    cur = mysql1.connection.cursor()
    resultValue = cur.execute("SELECT * FROM order_details order by item_price limit 3")
    if resultValue > 0:
        
        result_list = cur.fetchall() 
        fields_list = cur.description   # sql key name

    cur.close()
        #    mysql1.connection.close()
        #cur.close()
    column_list = []
    for i in fields_list:
        column_list.append(i[0])
    jsonData_list = []
    for row in result_list:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        
            jsonData_list.append(data_dict)
    return jsonify({'Top3Price Data': result_list})
        #cur.close()
@app.route('/last3orders')
def last3orders():
    cur = mysql1.connection.cursor()
    resultValue = cur.execute("SELECT * FROM order_details where order_timestamp >= DATE(NOW()) - INTERVAL 3 DAY")
    try:
        if resultValue > 0:
        
            result_list = cur.fetchall() 
            fields_list = cur.description   # sql key name
    
        #    mysql1.connection.close()
        #cur.close()
        column_list = []
        for i in fields_list:
            column_list.append(i[0])
        jsonData_list = []
        for row in result_list:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
        
                jsonData_list.append(data_dict)
        return jsonify({'Last3days Data': result_list})
    except mysql.connector.Error as err:
        print(err)
        cur.close()

@app.route("/readlist")
def readlist():
    #with open("my_list.txt",'r') as f :
    my_list=['A12345','A14576','A14579']
    cur = mysql1.connection.cursor()
    count = 0
    for i in my_list:
        acctnum = i
        resultValue = cur.execute("delete FROM order_details where acct_number ='%s' " %(acctnum))
        #print(resultValue)
        rowcount = cur.rowcount
        #cur.execute('select row_count() as rowcount')
        #rows = cur.fetchall()
        #rowcount = rows[0].get('rowcount', -1)
        count+=rowcount
    print(count)
    return render_template("list.html", len = len(my_list), my_list = my_list,count=count)

if __name__ == '__main__':
    app.run("0.0.0.0",port=5000)