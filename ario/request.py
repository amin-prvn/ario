from http.cookies import SimpleCookie


class Lazy:
    __slots__ = ('f',)

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, t=None):
        f = self.f
        if obj is None:
            return f
        val = f(obj)
        setattr(obj, f.__name__, val)
        return val


class Request:
    def __init__(self, environ):
        self.environ = environ

    @Lazy
    def content_length(self):
        return self.environ.get("CONTENT_LENGTH")

    @Lazy
    def content_type(self):
        content_type = self.environ.get("CONTENT_TYPE")
        if content_type:
            return content_type.split(';')[0]
        return None

    @Lazy
    def method(self):
        return self.environ['REQUEST_METHOD'].lower()

    @Lazy
    def path(self):
        return self.environ['PATH_INFO'].lower()

    @Lazy
    def cookies(self):
        cookie = SimpleCookie()
        if 'HTTP_COOKIE' in self.environ:
            cookie.load(self.environ['HTTP_COOKIE'])
        return cookie
