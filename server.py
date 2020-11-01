from flask import  Flask, render_template, request, redirect, url_for, sessions
from form import SearchForm
import mysql.connector
from movie import Movie

web = Flask(__name__)
web.config['SECRET_KEY'] = 'hoailam'

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='my_database'
)
cursor = mydb.cursor()


@web.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    film_ids1 = set()
    film_ids2 = set()
    film_ids3 = set()
    film_ids = set()

    if form.is_submitted():
        result = request.form
        title = result.get('title')
        year = result.get('year')
        director = result.get('director')
        search_by_title = 'select film_id from film where title = %s'
        search_by_year = 'select film_id from film where release_year like %s'
        search_by_director = 'select film_id from film f inner join director d on d.director_id = f.director_id where d.name = %s'

        if not title == '':
            cursor.execute(search_by_title, (title,))
            film_list1 = cursor.fetchall()
            for fl in film_list1:
                film_ids1.add(fl[0])
        if not year == '':
            pattern = "%" + year + "%"
            cursor.execute(search_by_year, (pattern,))
            film_list2 = cursor.fetchall()
            for fl2 in film_list2:
                film_ids2.add(fl2[0])
        if not director == '':
            cursor.execute(search_by_director, (director,))
            film_list3 = cursor.fetchall()
            for fl3 in film_list3:
                film_ids3.add(fl3[0])
        if (director == '' and year == '') or (director == '' and title == '') or (title == '' and year == '') or (
                title == '' and director == '' and year == ''):
            film_ids = film_ids1.union(film_ids2.union(film_ids3))
        elif not title == '' and not director == '' and not year == '':
            film_ids = film_ids1.intersection(film_ids2.intersection(film_ids3))
        else:
            film_ids = film_ids1.intersection(film_ids2).union(film_ids1.intersection(film_ids3)).union(
                film_ids2.intersection(film_ids3))
        id_info = list(film_ids)
        return redirect(url_for('show_search', id_info=id_info))
    return render_template('home.html', form=form)


@web.route('/search')
def show_search():
    film_ids = request.args.getlist('id_info')
    film_objects = []
    retrieve_info = 'select * from film where film_id = %s'
    for x in film_ids:
        cursor.execute(retrieve_info, (x,))
        movie_info = cursor.fetchone()
        film_objects += [Movie(movie_info[0], movie_info[1], movie_info[2], movie_info[4], movie_info[7])]
    search_result = film_objects
    return render_template('search.html', result=search_result)


# def choose_movie():
#     film_id = request.args.get('film_id')
#     return redirect(url_for(movie_show, film_id=film_id))


@web.route('/movie/<film_id>')
def movie_show(film_id):
    select_movie = 'select * from film where film_id = %s'
    cursor.execute(select_movie, (film_id,))
    result = cursor.fetchone()

    title = result[1]
    description = result[5]
    poster_url = result[7]
    trailer_url = result[8]
    return render_template('movie.html', title=title, description=description, poster_url=poster_url, trailer_url = trailer_url)


if __name__ == '__main__':
    web.run()