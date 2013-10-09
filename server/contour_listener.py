import os
import urlparse
from werkzeug.wrappers    import Request, Response
from werkzeug.routing     import Map, Rule
from werkzeug.exceptions  import HTTPException, NotFound
from werkzeug.wsgi        import SharedDataMiddleware
from werkzeug.utils       import redirect
from werkzeug.urls        import url_decode

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from simplejson import loads
class ContourPlotter(object):

  def __init__(self):
    self.thing = "thing"
    self.url_map = Map([
      Rule('/floorpng',endpoint='generate_png'),
      Rule('/floorsvg',endpoint='generate_svg'),
      Rule('/',endpoint='hello')
      ])
  def on_generate_svg(self,request,random_thing):
    return Response('Generating svg %s' % request.url)

  def on_generate_png(self,request):
    print 'yo'
    print request.headers.get('content-type')
    thing = request.form.copy().popitem()
    data = loads(thing[0])

    x=[]
    y=[]
    z=[]
    for d in data:
      x.append(float(d['X']))
      y.append(float(d['Y']))
      z.append(float(d['VelocityMag']))

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    print '%s' % x.__class__ #[0]['VelocityMag']
    print '%s' % x
    return Response('Generating png s')
  
  def on_hello(self,request):
    return Response('Hello World')

  def dispatch_request(self,request):
    adapter = self.url_map.bind_to_environ(request.environ)
    try:
      endpoint, values = adapter.match()
      return getattr(self, 'on_' + endpoint)(request, **values)
    except HTTPException, e:
      return e

  def wsgi_app(self,environ,start_response):
    request = Request(environ)
    response = self.dispatch_request(request)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response(environ,start_response)
  
  def __call__(self,environ,start_response):

    return self.wsgi_app(environ,start_response)

def create_app():
  app = ContourPlotter()
  return app

if __name__ == '__main__':
  from werkzeug.serving import run_simple
  app = ContourPlotter()
  run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

