Query On CSV Version 2.0 11/21/2017
------------------------------------
Target in the scenarios that users want to acquire information from CSV files without putting data into a dataset, we developed this python-based software to ask questions over huge amount of data(300 attributes, millions of rows).

General Usage Notes
------------------------------------
- Install an IDE for Python, e.g. Spyder or PyCharm
- Open 'test_query.py' 
- Declare file path (We don't have a user interface yet)
- Declare input query 
- Build index first (call build_index)
- Run 'test_query.py'

Query syntax
------------------------------------
- The input query should be a string ended with a semicolon (;).
- The logic operators (SELECT, FROM, WHERE, AND, OR, NOT, LIKE) are case-sensitive and expected to be uppercase.
- Use comma (,) to separate attributes in SELECT clause, files in FROM clause, conditions in WHERE clause.
- Leave at least ONE space on both sides for operator(>, >=, <, <=, =, <>, AND, OR, NOT, LIKE).
- For LIKE, the pattern should be in string format with single quotes (' ').
- Rename required for querying two or more tables


Example query:
------------------------------------
"SELECT movie_title, title_year, imdb_score FROM movies.csv WHERE ( movie_title LIKE '%Kevin%' AND imdb_score > 7 );

Result:
------------------------------------
['We Need to Talk About Kevin', '2011', '7.5']
['Kevin Hart: Laugh at My Pain', '2011', '7.5']


Example query 2:
------------------------------------
"SELECT M.movie_title, A.Award FROM movies.csv M, oscars.csv A WHERE A.Name LIKE '%Kevin%' AND A.Winner = 1 AND A.Award = 'Actor in a Leading Role' AND A.Name = M.actor_1_name AND M.title_year > 2000 AND M.budget > M.gross AND M.movie_title LIKE '%Superman%' ;"

Result:
------------------------------------
['Superman Returns', 'Actor in a Leading Role']

------------------------------------
Some queries are provided in the 'test_query.py'. 

Feel free to contact me: zc15@illinois.edu, if you have any issue in running the program.

Upcoming features
------------------------------------
- Handling query with at least two pairs of parentheses
- Handling query with arithmatic expression
- User interface
- Querying 4 tables
------------------------------------
Copyright 2017 GSON
