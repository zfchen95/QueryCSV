import main_V2 as sql
import time


# one table
sample_query1 = "SELECT movie_title, title_year, imdb_score " \
                "FROM movies.csv WHERE ( movie_title LIKE '%Kevin%' AND imdb_score > 7 ); "
test_query_1_1 = "SELECT movie_title, title_year, imdb_score, movie_facebook_likes, content_rating FROM movies.csv " \
                 "WHERE title_year > 2014 AND ( imdb_score > 8 OR movie_facebook_likes > 100000 ) AND content_rating <> 'R' AND content_rating <> '' AND NOT movie_title LIKE '%The%';"
# two table
sample_query2 = "SELECT A1.Year, A1.Film, A1.Award, A1.Name, A2.Award, A2.Name " \
                "FROM oscars.csv A1, oscars.csv A2 WHERE A1.Film <> '' AND A1.Winner = 1 " \
                "AND A2.Winner=1 AND A1.Award > A2.Award AND A1.Year > 2010 AND A1.Film = A2.Film;"
sample_query3 = "SELECT M.title_year, M.movie_title, A.Award, M.imdb_score, M.movie_facebook_likes " \
                "FROM movies.csv M, oscars.csv A WHERE A.Winner = 1 " \
                " AND M.movie_title = A.Film" \
                " AND ( M.imdb_score < 6 OR M.movie_facebook_likes < 10000 );"
test_query_2_1 = "SELECT M.title_year, M.movie_title, A.Award, M.imdb_score, M.movie_facebook_likes " \
                "FROM movies.csv M, oscars.csv A WHERE A.Winner = 1 " \
                " AND M.imdb_score < 6 AND ( M.movie_title = A.Film OR M.director_name = A.Name );"
test_query_2_2 = "SELECT * FROM movies.csv M, oscars.csv A WHERE A.Name LIKE '%Kevin%' AND A.Winner = 1 AND A.Award = 'Actor in a Leading Role' " \
              "AND A.Name = M.actor_1_name AND M.title_year > 2000 AND M.budget > M.gross AND M.movie_title LIKE '%Superman%' ;"
test_query_2_3 = "SELECT M.title_year, M.movie_title, M.director_name, M.imdb_score " \
                 "FROM movies.csv M, oscars.csv A WHERE M.title_year > A.Year AND M.director_name = A.Name AND M.imdb_score > 8 AND A.Winner = 1 AND M.title_year > 2000;"
test_query_2_4 = "SELECT M.movie_title, A.Award, M.language, M.country FROM movies.csv M, oscars.csv A WHERE A.Film = M.movie_title AND M.imdb_score > 7 AND ( A.Film LIKE '%Dallas%' OR A.Film LIKE '%New York%' );"

# three table
sample_query4 = "SELECT M.movie_title, M.title_year, M.imdb_score, A1.Name, A1.Award, A2.Name, A2.Award " \
                "FROM movies.csv M, oscars.csv A1, oscars.csv A2 WHERE A1.Award = 'Actor' AND A2.Award = 'Actress' " \
                "AND M.movie_title = A1.Film AND M.movie_title = A2.Film ;"

query_input = "SELECT M.movie_title, A.Award FROM movies.csv M, oscars.csv A WHERE A.Name LIKE '%Kevin%' AND A.Winner = 1 AND A.Award = 'Actor in a Leading Role' AND A.Name = M.actor_1_name AND M.title_year > 2000 AND M.budget > M.gross AND M.movie_title LIKE '%Superman%' ;"

# query_list = [sample_query1, sample_query2, sample_query3, sample_query4, test_query_1_1, test_query_2_1, test_query_2_2, test_query_2_3, test_query_2_4]
query_list = [sample_query1]
for single_query in query_list:
    start = time.time()
    query_output = sql.execute_query(single_query)
    end = time.time()
    try:
        for res_row in query_output:
            print(res_row)
    except:
        print('query output is not defined')
    print("running time", end - start)
