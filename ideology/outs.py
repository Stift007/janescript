



from sys import *
import datetime
import typing

class __POSIXPATH:
	sep = "/"
	@staticmethod
	def join(*a):
		return "/".join(a)

	@staticmethod
	def base(__path):
		return __path.split("/")[-1]
	
	@staticmethod
	def dirname(__path):
		return "/".join(__path.split("/")[:-1])


	@staticmethod
	def splitext(__path):
		b = __POSIXPATH.base(__path)
		ext = b.split(".")[-1]
		rest = ".".join(b.split(".")[:-1])
		return (rest, ext)

	@staticmethod
	def split(__path):
		return __path.split("/")

class __NTPATH:
	sep = "\\"
	@staticmethod
	def join(*a):
		return "\\".join(a)

	@staticmethod
	def base(__path):
		return __path.split("\\")[-1]
	
	@staticmethod
	def dirname(__path):
		return "\\".join(__path.split("\\")[:-1])

	@staticmethod
	def splitext(__path):
		b = __NTPATH.base(__path)
		ext = b.split(".")[-1]
		rest = ".".join(b.split(".")[:-1])
		return (rest, ext)

	@staticmethod
	def split(__path):
		return __path.split("\\")


class __TIMEREP(object):

	def __init__(this):
		dtclass = datetime.datetime
		delta = datetime.timedelta
	
	@typing.overload
	def elapsedsince(this, tstamp: typing.Union[int, float]):...

	@typing.overload
	def elapsedsince(this, dateobj: datetime.datetime):...

	def elapsedsince(this, dt):
		if isinstance(dt, datetime.datetime):
			res = (datetime.datetime.now() - dt).milliseconds
			
		elif isinstance(dt, typing.Union[int, float]):
			res = datetime.datetime.now().timestamp() - dt
		return res

	def time(this):
		return this.system()
	
	def system(this):
		return datetime.datetime.now().timestamp()

#include <_os>
import sys

if sys.platform == "win32":
	path = __NTPATH

else:
	path = __POSIXPATH

CURPATH = "."
time = __TIMEREP()
from jinja2 import *
#include <os>
#include <octane>

template_path = path.join(path.dirname(__file__), 'templates')


jinja_env = Environment(loader=FileSystemLoader(template_path),
                                 autoescape=True)


def render_template(template_name,request, **context):
    t = jinja_env.get_template(template_name)
    return HTTPResponse(request, t.render(context), content_type='text/html')


import cgi
import typing

class IterLike:
    def __init__(this, initial_values):
        this.vals = initial_values

    def add(this, *vals):
        this.vals.extend(vals)

    def find(this, callable, item, *, default=None):
        for anything in this:
            if callable(anything): return anything
        return default

class Post:
    def __init__(this, data):
        this.data = data

    def get(this, key, default=[""]):
        value = this.data.get(key, default)
        if type(value) == str:
            value = cgi.escape(value)
        return value

    def set(this, key, value):
        this.data[key] = value

    def __setitem__(this, key, val):this.set(key, val)
    def __getitem__(this, key): return this.get(key)

    def __iter__(this):
        for k, v in this.data:
            yield (k, v)


class Request:
    def __init__(this, environ, start_response):
        this.environ = environ
        this.host = environ["HTTP_HOST"]
        this.user_agent = environ["HTTP_USER_AGENT"]
        this.language = environ.get("LANG")
        this.method = environ.get("REQUEST_METHOD")
        this.path = environ.get("PATH_INFO")
        this.gateway = environ.get("GATEWAY_INTERFACE")
        this.port = environ.get("SERVER_PORT")
        this.remote = environ.get("REMOTE_HOST")
        this.content_type = environ.get("CONTENT_TYPE")
        this.content_length = environ.get("CONTENT_LENGTH")
        this.body = environ.get("BODY")
        this.query = environ.get("QUERY_STRING")
        this.protocol = environ.get("SERVER_PROTOCOL")
        this.software = environ.get("SERVER_SOFTWARE")
        this.start_response = start_response

        this.parse_qs()

    def parse_qs(this):
        if this.method != "POST":
            return
        environ = this.environ
        this.post = Post({})
        field_storage = cgi.FieldStorage(
            fp = environ["wsgi.input"],
            environ = environ,
            keep_blank_values = True
        )
        for item in field_storage.list:
            if not item.filename:
                this.post[item.name] = item.value
            else:
                this.post[item.name] = item

class Route:
    def __init__(this, path, fun, method):
        this.path = path
        this.func = fun
        this.method = method
    
    def match(this, path, method):
        return this.path == path and this.method == method

class Router:
    def __init__(this, routes=None):
        this.routes = list(routes) if routes else []

    def add_route(this, path):
        this.routes.append(path)

    def get_route(this, path, method="GET"):
        for i in this.routes:
            if i.match(path, method):
                return i.func
        return None

class BaseResponse:
    def __init__(this, request: Request, status_code, content_type):
        this.headers = IterLike([])
        this.status_code = status_code
        this.start_response: t.Callable = request.start_response
        this.content_type = content_type
        this.response_content = []

    def make_response(this):
        this.start_response(this.status_code, this.headers.vals)
        return this.response_content

class HTTPResponse(BaseResponse):
    def __init__(this, request: Request, content, status_code = "200 OK", content_type="text/plain"):
        super().__init__(request, status_code, content_type)
        if type(content) == str:
            content = content.encode()
        elif type(content) != bytes:
            content = bytes(content)
        
        this.response_content.append(content)

class ErrorResponse(HTTPResponse):
    def __init__(this, request, error_code="500 Internal Server Error", details="The Server encountered an internal Error and was unable to complete your Request"):
        super().__init__(request, details, error_code, "text/html")

#include <_octane>
#include <voyage>
from wsgiref.simple_server import *
import json

request = None

class HTTPServer:
    def __init__(this):
        this.router = Router()

    def endpoint(this, rule, **kwargs):
        def predicate(func):
            this.router.add_route(Route(rule, func, kwargs.get("method", "GET").upper()))
        return predicate

    def __call__(this, environ, start_response):
        global request
        request = Request(environ, start_response)
        try:
            func = this.router.get_route(request.path)
            if func:
                response: BaseResponse = func(request)
                return response.make_response()
            else:
                return ErrorResponse(request, "404 Not Found", f"The Route {request.path} was not found").make_response()
        except Exception as e:
            print(e)
            return ErrorResponse(request, details=e).make_response()

def text(t, scode="200 OK"):
    return HTTPResponse(request, t, scode)

def template(tname, scode="200 OK", **context):
    try:
        env = FSLoader(".")
        templ = env.get_template(tname)
        return HTTPResponse(request, templ.render(context), scode, "text/html")
    except Exception as e:
        print(ErrorResponse(request, details=str(e)))
        #return ErrorResponse(request, details=str(e)).make_response()


def jsonify(objects: dict={}, **kwargs):
    code = json.dumps(dict if dict else kwargs)
    return HTTPResponse(request, code, "200 OK", content_type="application/json")

def start(app: HTTPServer, host="127.0.0.1", port=4567):
    server = make_server(host, port, app)
    server.serve_forever()
#include <octane>
#include <jinja2jns>
import requests
import json
import requests_oauthlib

def getYoutubeVideos():
    r = requests.get("https://www.googleapis.com/youtube/v3/search?key=AIzaSyBG3xQFADdzJ7t4yIqhy3lloHzwajeXG6o&channelId=UCKySeviC7nVGyWM8T3sMkXA&part=snippet,id&order=date&maxResults=3")
    #r = requests.get("https://www.googleapis.com/youtube/v3/search?key=AIzaSyBG3xQFADdzJ7t4yIqhy3lloHzwajeXG6o&channelId=UCeAgRH-t9a70zF3LvMjl1qQ&part=snippet,id&order=date&maxResults=3")
    with open("res","wb") as f:
        f.write(r.content)

def getTweets():
    consumer_key = "JMEgEp3sg6puLwqeNH7ZuhlrY"
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPHFhAEAAAAAd1wdiZfTjg1RPR0Xhu2d1%2FboHBY%3DjqLt5CG7xOkoagOGeQ28EdOBa9kfZRnhSnfIkBn9pCw3Rn8u1t"
    consumer_secret = "co64U6MIZxrpXn3yKGjnN4saTksMXV362aR7cth2uNc88ChrQD"
    ID = "1471973012119465988"
    params = {"ids": ID, "tweet.fields": "created_at"}


app = HTTPServer()


@app.endpoint("/")
def root(req):
    with open("youtube.json") as f:
        items = json.load(f)
    return render_template("index.html", req,youtube=items["items"])

@app.endpoint("/youtube.json")
def yt(req):
    return HTTPResponse(req, open("youtube.json").read(), content_type="application/json")
getTweets()
start(app)