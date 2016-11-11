def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain')]
    query = environ['QUERY_STRING']
    res = '\n'.join(query.split('&'))
    start_response(status, headers)
    return res