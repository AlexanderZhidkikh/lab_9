from flask import Flask, render_template, url_for, redirect, request
import sqlalchemy as db




def searchdd(serchText):

    select_query = db.select(cities).where(cities.columns.town == serchText)
    select_result = connection.execute((select_query))
    searchCity =select_result.fetchall()
    if len(searchCity) ==0:
        select_query = db.select(cities).where(cities.columns.visit_date == serchText)
        select_result = connection.execute((select_query))
        searchBook = select_result.fetchall()
    return searchCity


app = Flask(__name__)


try:
    engine = db.create_engine('mysql+pymysql://root:ason121245@localhost:3306/my_database')
    connection = engine.connect()
    print("Connect DB")
except Exception as ex:
    print("ERROR Connect DB")
    print(ex)

metadata = db.MetaData()
cities = db.Table('cities', metadata,
                 db.Column('city_id', db.Integer, primary_key=True),
                 db.Column('town', db.Text),
                 db.Column('visit_date', db.Text))

metadata.create_all(engine)

insertion_query = cities.insert().values([
    {"town":"Москва", "visit_date":" 1 сентября 2022"},
    {"town":"Сочи", "visit_date":" 2 сентября 2022"},
    {"town":"Архангельск", "visit_date":" 3 сентября 2022"},
    {"town":"СПб", "visit_date":" 4 сентября 2022"},
    {"town":"Екатеринбург", "visit_date":" 5 сентября 2022"},
    {"town":"Анапа", "visit_date":" 6 сентября 2022"},
    {"town":"Тальяти", "visit_date":" 7 сентября 2022"},
    {"town":"Оренбург", "visit_date":" 8 сентября 2022"},


])
#connection.execute(insertion_query)

selall = db.select(cities)
selres = connection.execute(selall)
allСities = selres.fetchall()

@app.route('/', methods =["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get('clear') =='Clear':
            d = searchdd("s")
            return render_template('index.html', allСities=d, len=len(d))
        elif request.form.get('all') =='All List':
            render_template('index.html' , allСities = allСities, len = len(allСities))
        elif request.form.get('searchBtn') == 'Search':
            a = request.form.get("search")
            d = searchdd(a)
            return render_template('index.html' , allСities = d, len = len(d))
    return render_template('index.html' , allСities = allСities, len = len(allСities))

if __name__ == '__main__':
    app.run(debug=True, port=5001 )