from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'world'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

class CountryResource(Resource):
    def get(self, code=None):
        cur = mysql.connection.cursor()
        if code:
            cur.execute("SELECT * FROM Country WHERE Code = %s", (code,))
            country = cur.fetchone()
            cur.close()
            if country:
                return jsonify(country)
            else:
                return {"message": "Country not found"}, 404
        else:
            cur.execute("SELECT * FROM Country")
            countries = cur.fetchall()
            cur.close()
            return jsonify(countries)

    def post(self):
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Country (Code, Name, Continent, Region, SurfaceArea, IndepYear, Population, LifeExpectancy, GNP, GNPOld, LocalName, GovernmentForm, HeadOfState, Capital, Code2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (data['Code'], data['Name'], data['Continent'], data['Region'], data['SurfaceArea'], data['IndepYear'], data['Population'], data['LifeExpectancy'], data['GNP'], data['GNPOld'], data['LocalName'], data['GovernmentForm'], data['HeadOfState'], data['Capital'], data['Code2']))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Country added successfully"})

    def put(self, code):
        data = request.json
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Country SET Name = %s, Continent = %s, Region = %s, SurfaceArea = %s, IndepYear = %s, Population = %s, LifeExpectancy = %s, GNP = %s, GNPOld = %s, LocalName = %s, GovernmentForm = %s, HeadOfState = %s, Capital = %s, Code2 = %s WHERE Code = %s",
                    (data['Name'], data['Continent'], data['Region'], data['SurfaceArea'], data['IndepYear'], data['Population'], data['LifeExpectancy'], data['GNP'], data['GNPOld'], data['LocalName'], data['GovernmentForm'], data['HeadOfState'], data['Capital'], data['Code2'], code))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Country updated successfully"})

    def delete(self, code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Country WHERE Code = %s", (code,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Country deleted successfully"})

api.add_resource(CountryResource, '/countries', '/countries/<string:code>')

if __name__ == '__main__':
    app.run(debug=True)
