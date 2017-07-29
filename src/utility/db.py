import csv

from src.strings import queries
from src.utility import neo4jdriver

_record_time = False


# todo: utilize progressBar in this file

# creates indexes for the labels
def create_index(label, label_id):
    print("create_index start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.index_query_create.format(label, label_id))
    print("create_index end")  # todo: use Logger Class


def create_movies(path):
    print("create_movies start")  # todo: use Logger Class
    data = []
    with open(path, 'rb') as movies:
        csvr = csv.DictReader(movies, delimiter=',', quotechar='"')
        for row in csvr:
            data.append({"movie_id": int(row['movieId']), "title": row['title'], "genres": row['genres']})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.movie_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.movie_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_movies end")  # todo: use Logger Class


def create_links(path):
    print("create_links start")  # todo: use Logger Class
    data = []
    with open(path, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[0]), "imdbId": row[1], "tmdbId": row[2]})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.link_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.link_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_links end")  # todo: use Logger Class


def create_ratings(path):
    print("create_ratings start")  # todo: use Logger Class
    data = []
    with open(path, 'rb') as ratings:
        csvr = csv.DictReader(ratings, delimiter=',', quotechar='"')
        for row in csvr:
            data.append({"movie_id": int(row['movieId']),
                         "user_id": int(row['userId']),
                         "rating": float(row['rating']),
                         "timestamp": row['timestamp']})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.rating_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.rating_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_ratings end")  # todo: use Logger Class


def create_tags(path):
    print("create_tags start")  # todo: use Logger Class
    data = []
    with open(path, 'rb') as csv_file:
        iter_reader = iter(csv.reader(csv_file, delimiter=',', quotechar='"'))
        next(iter_reader)
        for row in iter_reader:
            data.append({"movie_id": int(row[1]), "user_id": int(row[0]), "tag": row[2], "timestamp": float(row[3])})
            if len(data) == 10000:
                with neo4jdriver.session.begin_transaction() as tx:
                    tx.run(queries.tag_query_create, data=data)
                    tx.commit()
                    del data[:]
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.tag_query_create, data=data)
        tx.commit()
        del data[:]
    print("create_tags end")  # todo: use Logger Class


# get movie by id
def get_movie_by_id(movie_id):
    print("return_movie start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_query_get_by_id, movie_id=movie_id)
        if not len(records.data()):
            print "No record!"  # todo: use Logger Class
        else:
            for record in records:
                title = record[0]["title"]
                print(title)  # todo: use Logger Class
    print("return_movie end")  # todo: use Logger Class


# get average of ratings of specific movie
def get_avg_rating_of_movie(movie_id):
    print("get_avg_rating_of_movie start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_query_get_avg_rating, movie_id=movie_id)
        if not len(records.data()):
            print "No record!"  # todo: use Logger Class
        else:
            for record in records:
                title = record["title"]
                avg = record["rating_avg"]
                print("%s has %s average rating" % (title, avg))  # todo: use Logger Class
    print("get_avg_rating_of_movie end")  # todo: use Logger Class


# get average of ratings of users
def get_avg_rating_of_user(user_id):
    print("get_avg_rating_of_user start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.user_query_get_avg_rating, user_id=user_id)
        rating_mean = 0
        if not len(records.data()):
            print "No record!"  # todo: use Logger Class
        else:
            for record in records:
                # user_id = record["user_id"]
                rating_mean = record["rating_avg"]
                # print("%s has %s average rating" % (user_id, rating_mean))  # todo: use Logger Class
    print("get_avg_rating_of_user end")  # todo: use Logger Class
    return rating_mean


# get average of ratings of all users
def get_avg_rating_of_all_user():
    users_rating_avg = {}
    # print("get_avg_rating_of_user start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.user_query_get_all_avg_rating)
        data = records.data()
        if len(data):
            for record in data:
                user_id = record["user_id"]
                rating_mean = record["rating_avg"]
                users_rating_avg[user_id] = rating_mean
        else:
            print "No record!"  # todo: use Logger Class
    print("get_avg_rating_of_user end")  # todo: use Logger Class
    return users_rating_avg


#
def create_dynamic_similarity(data):
    print("create_dynamic_similarity start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        tx.run(queries.movie_query_create_dynamic_similarity, data=data)
        tx.commit()
    print("create_dynamic_similarity end")  # todo: use Logger Class


#
def create_static_similarity():
    pass


#
def get_all_movies():
    pass


#
def get_by_ratings_movie_ids(movie1_id, movie2_id):
    # print("get_by_ratings_movie_ids start")  # todo: use Logger Class
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_movie_query_adjusted_cosine, movie1_id=movie1_id, movie2_id=movie2_id)
    # print("get_by_ratings_movie_ids end")  # todo: use Logger Class
    return records.data()


# get count of movie
def get_movie_ids():
    print("get_movie_count start")  # todo: use Logger Class
    data = []
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_query_get_all_movie_ids)
        for record in records:
            data.append(record["movie_id"])
    print("get_movie_count end")  # todo: use Logger Class
    return data


# returns list of (otherMovieId, similarity) of movie
def get_prediction_by_user_and_movie_id(user_id, movie_id, k_neighbours=5):
    print("get_prediction_by_user_and_movie_id start")  # todo: use Logger Class
    prediction = -1
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.user_movie_query_get_prediction,
                         movie_id=movie_id, user_id=user_id, k_neighbours=k_neighbours)
        for record in records:
            prediction = record["prediction"]
    print("get_prediction_by_user_and_movie_id end")  # todo: use Logger Class
    return prediction


# get movie rating count by movie id
def get_movie_rating_count(movie_id):
    count = -1
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.movie_rating_count_query_by_id, movie_id=movie_id)
        data = records.data()
        if not len(data):
            print "No record!"  # todo: use Logger Class
        else:
            count = data[0]['count']
    return count


# get similarities of k-nearest movie by movie id
def get_similarities_by_movie_k_n(movie_id, k_neighbours):
    result = []
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.similarities_by_movie_neighbour,
                         movie_id=movie_id, k_neighbours=k_neighbours)
        data = records.data()
        if not len(data):
            print "No record!"  # todo: use Logger Class
        else:
            for row in data:
                movie2_id = row['movie2_id']
                sim = row['sim']
                result.append((movie2_id, sim))
    return result


# get similarities by movie id
def get_similarities_by_movie(movie_id):
    result = []
    with neo4jdriver.session.begin_transaction() as tx:
        records = tx.run(queries.similarities_by_movie,
                         movie_id=movie_id)
        data = records.data()
        if not len(data):
            print "No record!"  # todo: use Logger Class
        else:
            for row in data:
                movie2_id = row['movie2_id']
                sim = row['sim']
                result.append((movie2_id, sim))
    return result