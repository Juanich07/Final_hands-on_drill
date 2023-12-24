from flask import Flask, Response, make_response, jsonify, request, render_template
from flask_mysqldb import MySQL
import dicttoxml

app = Flask(__name__, template_folder='templates')

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "world"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def generate_xml_response(results):
    xml_data = dicttoxml.dicttoxml(results)
    return Response(xml_data, mimetype='text/xml')

def data_fetch(query):
    try:
        format_requested = request.args.get('format') 
        cur = mysql.connection.cursor()
        cur.execute(query)
        
        results = cur.fetchall()
        
        if format_requested and format_requested.lower() == 'xml':
            xml_data = generate_xml_response(results)
            return xml_data
        else:
            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

# Render HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_city', methods=['GET'])
def add_city_form():
    return render_template('add_city.html')

@app.route('/edit_city/<int:id>', methods=['GET'])
def edit_city_form(id):
    return render_template('edit_city.html', city_id=id)

@app.route('/delete_city/<int:id>', methods=['GET'])
def delete_city_form(id):
    return render_template('delete_city.html', city_id=id)

@app.route('/cities', methods=['GET'])
def get_cities():
    query = "SELECT * FROM world.city"
    result = data_fetch(query)
    return result

@app.route('/cities/<int:id>', methods=['GET'])
def get_city_by_id(id):
    query = f"SELECT * FROM world.city WHERE ID = {id}"
    result = data_fetch(query)
    return result

@app.route('/countries', methods=['GET'])
def get_countries():
    query = "SELECT * FROM world.country"
    result = data_fetch(query)
    return result

@app.route('/country_languages', methods=['GET'])
def get_country_languages():
    query = "SELECT * FROM world.countrylanguage"
    result = data_fetch(query)
    return result

@app.route('/cities', methods=['POST'])
def add_city():
    try:
        info = request.get_json()
        print("Received JSON:", info)
        name = info.get("name")
        country_code = info.get("country_code")
        district = info.get("district")
        population = info.get("population")
        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO world.city 
            (Name, CountryCode, District, Population) 
            VALUES (%s, %s, %s, %s)""",
            (name, country_code, district, population)
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()

        return make_response(
            jsonify({"message": "City added successfully", "rows_affected": rows_affected}),
            201
        )

    except Exception as e:
        print("Error adding city:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/cities/<int:id>', methods=['PUT'])
def update_city(id):
    try:
        cur = mysql.connection.cursor()
        info = request.get_json()
        print("Received JSON:", info)
        name = info.get("name")
        country_code = info.get("country_code")
        district = info.get("district")
        population = info.get("population")
        cur.execute(
            """ UPDATE world.city SET 
            Name = %s, CountryCode = %s, District = %s, Population = %s
            WHERE ID = %s """,
            (name, country_code, district, population, id),
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": "City updated successfully", "rows_affected": rows_affected}
            ),
            200,
        )
    except Exception as e:
        print("Error updating city:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/cities/<int:id>', methods=['DELETE'])
def delete_city(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM world.city where ID = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "City deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

if __name__ == "__main__":
    app.run(debug=True)

