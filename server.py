from flask import Flask, render_template, request, redirect, url_for, session
from form import SearchForm, LoginSignupForm, LoginForm, SignUpForm, UserRating
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

# -------------------------HOME PAGE-------------------------
@web.route("/", methods=["GET", "POST"])
def home():
    search_form = SearchForm()
    login_signup_form = LoginSignupForm()
    if not session.get("username") is None:
        username = session["username"]
    else:
        username = None

    film_ids1 = set()
    film_ids2 = set()
    film_ids3 = set()

    if login_signup_form.is_submitted():
        if login_signup_form.login.data:
            return redirect("login")
        if login_signup_form.signup.data:
            return redirect("signup")

    if search_form.is_submitted():

        result = request.form
        title = result.get("title")
        year = str(result.get("year"))
        director = result.get("director")
        search_by_title = "select film_id from film where title = %s"
        search_by_year = "select film_id from film where release_year like %s"
        search_by_director = "select film_id from film f inner join director d on d.director_id = f.director_id where d.name = %s"

        if not title == "":
            cursor.execute(search_by_title, (title,))
            film_list1 = cursor.fetchall()
            for fl in film_list1:
                film_ids1.add(fl[0])
        if not year == "":
            pattern = "%" + year + "%"
            cursor.execute(search_by_year, (pattern,))
            film_list2 = cursor.fetchall()
            for fl2 in film_list2:
                film_ids2.add(fl2[0])
        if not director == "":
            cursor.execute(search_by_director, (director,))
            film_list3 = cursor.fetchall()
            for fl3 in film_list3:
                film_ids3.add(fl3[0])
        if (director == "" and year == "") or (director == "" and title == "") or (title == "" and year == "") or (
                title == "" and director == "" and year == ""):
            film_ids = film_ids1.union(film_ids2.union(film_ids3))
        elif not title == "" and not director == "" and not year == "":
            film_ids = film_ids1.intersection(film_ids2.intersection(film_ids3))
        else:
            film_ids = film_ids1.intersection(film_ids2).union(film_ids1.intersection(film_ids3)).union(
                film_ids2.intersection(film_ids3))
        id_info = list(film_ids)
        return redirect(url_for("show_search", id_info=id_info))
    return render_template("home.html", search_form=search_form, login_signup_form=login_signup_form, username=username)
# ---------------------------LOG IN--------------------------------
@web.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    check_sign_up = request.args.get("check_sign_up")

    if login_form.is_submitted():
        result = request.form

        username = result.get("username")
        password = result.get("password")

        retrieve_user_info = "select * from user where username = %s"
        cursor.execute(retrieve_user_info, (username,))
        user_info = cursor.fetchone()
        if user_info and username == user_info[0] and password == user_info[1]:
            session["username"] = username #may be can use for refactoring
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            error = "Wrong Username or Password"
            return render_template("login.html", login_form=login_form, error=error)
    return render_template("login.html", login_form=login_form)
# ------------------SIGN UP---------------------------------
@web.route("/signup", methods=["GET", "POST"])
def signup():
    signup_form = SignUpForm()

    if signup_form.is_submitted():
        result = request.form

        username = result.get("username")
        password = result.get("password")
        cf_password = result.get("confirm_password")

        find_existing_user = "select * from user where username = %s"
        cursor.execute(find_existing_user, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            existing_user_error = "Existed username"
            return render_template("signup.html", signup_form=signup_form, error=existing_user_error)
        else:
            if len(password) < 6:
                password_error = "Password must have at least 6 characters"
                return render_template("signup.html", signup_form=signup_form, error=password_error)
            elif password != cf_password:
                cf_error = "Passwords must match"
                return render_template("signup.html", signup_form=signup_form, error=cf_error)
            else:
                insert_user = "insert into user (username, password) values (%s, %s)"
                cursor.execute(insert_user, (username, password))
                mydb.commit()
                return redirect("login")
    return render_template("signup.html", signup_form=signup_form)
# -------------------LOG OUT-------------------------------------
@web.route("/logout")
def log_out():
    session.pop("logged_in", None)
    session.pop("username", None)
    return redirect(url_for("home"))
# ----------SEARCH RESULT------------------------------------------------
@web.route("/search", methods=["GET", "POST"])
def show_search():
    login_signup_form = LoginSignupForm()
    if not session.get("username") is None:
        username = session["username"]
    else:
        username = None
    if login_signup_form.is_submitted():
        if login_signup_form.login.data:
            return redirect("login")
        if login_signup_form.signup.data:
            return redirect("signup")
    film_ids = request.args.getlist("id_info")
    film_objects = []
    retrieve_info = "select * from film where film_id = %s"
    for x in film_ids:
        cursor.execute(retrieve_info, (x,))
        movie_info = cursor.fetchone()
        film_objects += [Movie(movie_info[0], movie_info[1], movie_info[2], movie_info[4], movie_info[7])]
    search_result = film_objects
    return render_template("search.html", result=search_result, cnt=len(search_result), login_signup_form=login_signup_form, username=username)


# def choose_movie():

#     film_id = request.args.get("film_id")
#     return redirect(url_for(movie_show, film_id=film_id))

# ----------------------MOVIE PAGE--------------------------------
@web.route("/movie/<film_id>", methods=["GET", "POST"])
def movie_show(film_id):
    login_signup_form = LoginSignupForm()
    if not session.get("username") is None:
        username = session["username"]
    else:
        username = None
    if login_signup_form.is_submitted():
        if login_signup_form.login.data:
            return redirect("login")
        if login_signup_form.signup.data:
            return redirect("signup")
    select_movie = "select * from film where film_id = %s"
    cursor.execute(select_movie, (film_id,))
    result = cursor.fetchone()

    # select_movie_2 = "select * from genre where film_id = %s"
    # cursor.execute(select_movie_2, (film_id,))
    # result_2 = cursor.fetchone()

    # film_stars = []
    # search_star = "select * from star JOIN film_star ON film_star.star_id=star.star_id WHERE film_star.film_id = %s"
    # for x in film_ids:
    #     cursor.execute(search_star, (x,))
    #     movie_info = cursor.fetchone()
    #     film_stars += [Star(movie_info[2])]
    # result_3 = film_stars

    title = result[1]
    release_year = result[3]
    # genre = result_2[2]
    # star = result_3
    length = result[4]
    description = result[5]
    poster_url = result[7]
    trailer_url = result[8]

    if not session.get("logged_in") is None:
        user_rating_form = UserRating()
        if user_rating_form.is_submitted():
            rating = request.form
            user_rating = rating.get("rating")
            import_sql = "insert into user_rating (username, film_id, rating) values (%s, %s, %s)"
            val = (session["username"], film_id, user_rating)
            cursor.execute(import_sql, val)
            mydb.commit()
        return render_template("movie.html", title=title, description=description, poster_url=poster_url, trailer_url=trailer_url, length=length, release_year=release_year, user_rating_form=user_rating_form, login_signup_form=login_signup_form, username=username)
    return render_template("movie.html", title=title, description=description, poster_url=poster_url, length=length, release_year=release_year, trailer_url=trailer_url, login_signup_form=login_signup_form, username=username)


if __name__ == "__main__":
    web.run()

