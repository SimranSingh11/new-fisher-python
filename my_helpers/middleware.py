class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        print("\n response : ", response)
        return response



# ============================================================ #
# QueryCountDebugMiddleware: 
# ============================================================ #

class QueryCountDebugMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        from django.db import connection
        from base.utils import p_print

        response = self.get_response(request)

        console_print = True

        total_time = 0
        q_list = list()

        for query in connection.queries:
            query_time = query.get('time')
            if query_time is None:
                # django-debug-toolbar monkeypatches the connection
                # cursor wrapper and adds extra information in each
                # item in connection.queries. The query time is stored
                # under the key "duration" rather than "time" and is
                # in milliseconds, not seconds.
                query_time = query.get('duration', 0) / 1000
            total_time += float(query_time)
            q_list.append(query)

        if console_print:
            print("\n==================== QueryCountDebugMiddleware ================================\n")
            print("API: ",request.path)
            print("Queries run: ",len(connection.queries))
            print("Total seconds: ",total_time)
            p_print("Queries: ",q_list)
            print("\n==================== !QueryCountDebugMiddleware ================================\n")

        return response

# ============================================================ #

