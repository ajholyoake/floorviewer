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
import sys
from scipy.interpolate import griddata
import urllib
import numpy.ma as ma
import cStringIO
import msvcrt

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
    xr = [np.amin(x),np.amax(x)]
    yr = [np.amin(y),np.amax(y)]
    
    xi = np.linspace(xr[0],xr[1],100)
    yi = np.linspace(yr[0],yr[1],100)
    zi = griddata((x,y),z,(xi[None,:],yi[:,None]),method='cubic')
    print '%s %s %s' %( xi.size, yi.size, zi.size)
    fig = plt.figure()
    CS = plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
    CS = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)
    plt.colorbar()
    plt.scatter(x,y,marker='o',c='b',s=5)
    plt.xlim(xr[0],xr[1])
    plt.ylim(yr[0],yr[1])
    plt.title('Thing')
    plt.show()
    sio = cStringIO.StringIO()
    fig.savefig(sio,format="png")
    string = sio.getvalue() 
    print 'Sending response'
    return Response(string.encode("base64").strip())
  
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
  run_simple('dev-performanceanalysis', 5000, app, use_debugger=True, use_reloader=True)

