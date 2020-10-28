import mysql.connector
import pandas as pd

director = pd.read_csv('./data/director.csv')
film = pd.read_csv('./data/film.csv')
film_star = pd.read_csv('./data/film_star.csv')
genre = pd.read_csv('./data/genre.csv')
star = pd.read_csv('./data/star.csv')

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='my_database',
    auth_plugin='mysql_native_password'
)

cursor = mydb.cursor()

# insert_dir = 'INSERT INTO director (director_id, name) VALUES (%s, %s)'
# val_dir = [(int(director['director_id'][i]), director['name'][i]) for i in range(len(director))]

# cursor.executemany(insert_sql, val)

# insert_film = 'insert into film (film_id, title, certificate, release_year, length, description, rating, director_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
# val_film = [(int(film['film_id'][i]), film['title'][i], film['certificate'][i], film['release_year'][i], film['length'][i], film['description'][i], int(film['rating'][i]), int(film['director_id'][i])) for i in range(len(film))]

# insert_film_star = 'insert into film_star (film_id, star_id) values (%s, %s)'
# val_film_star = [(int(film_star['film_id'][i]), int(film_star['star_id'][i])) for i in range(len(film_star))]

# insert_genre = 'insert into genre (film_id, genre) values (%s, %s)'
# val_genre = [(int(genre['film_id'][i]), genre['genre'][i]) for i in range(len(genre))]
#
# insert_star = 'insert into star (star_id, name) values (%s, %s)'
# val_star = [(int(star['star_id'][i]), star['name'][i]) for i in range(len(star))]
#
# cursor.executemany(insert_film, val_film)
# cursor.executemany(insert_genre, val_genre)
# cursor.executemany(insert_star, val_star)
# cursor.executemany(insert_film_star, val_film_star)

sql = 'update film set rating = %s where film_id = %s'
val = [(float(film['rating'][i]) ,int(film['film_id'][i])) for i in range(len(film))]
cursor.executemany(sql, val)

mydb.commit()
mydb.close()