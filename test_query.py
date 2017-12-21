import main_V3 as sql
import time


sample_query = "SELECT B.name, B.postal_code, R.review_id, R.stars, R.useful FROM business.csv B, review.csv R " \
               "WHERE B.city = 'Champaign' AND B.state = 'IL' AND B.business_id = R.business_id;"
query_list = [sample_query]
for single_query in query_list:
    start = time.time()
    query_output = sql.execute_query(single_query)
    end = time.time()
    # try:
    #     for res_row in query_output:
    #         print(res_row)
    # except:
    #     print('query output is not defined')
    print("Run time", end - start)
    print('Length of output', len(query_output))
