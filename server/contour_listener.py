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

from simplejson import loads,dumps
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
    d = loads(thing[0])
    ret = [] #returns three png things
    X = [];
    Y = [];
    Z = [];
    Zi = [];
    plotx = [float("Inf"),float("-Inf")]
    ploty = [float("Inf"),float("-Inf")]

    for i in range(0,2):
      if len(d[i]) > 0:
        x=[]
        y=[]
        z=[]
        for f in d[i]:
          x.append(float(f['X']))
          y.append(float(f['Y']))
          z.append(float(f['Z']))

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)

        X.append(x);
        Y.append(y);
        Z.append(z);
        plotx[0] = min(plotx[0],np.amin(x));
        plotx[1] = max(plotx[1],np.amax(x));
        ploty[0] = min(ploty[0],np.amin(y));
        ploty[1] = max(ploty[1],np.amax(y));

      else:
        X.append(np.array([]));
        Y.append(np.array([]));
        Z.append(np.array([]));
    
    xi = np.linspace(plotx[0],plotx[1],100)
    yi = np.linspace(ploty[0],ploty[1],100)

    for i in range(0,2):
      if X[i].size > 0: 
        Zi.append(griddata((X[i],Y[i]),Z[i],(xi[None,:],yi[:,None]),method='cubic'))
      else:
        Zi.append(np.array([]))

    if Zi[0].size > 0 and Zi[1].size > 0:
      Zi.append(np.subtract(Zi[1],Zi[0]))
    else:
      Zi.append(np.array([]))

    for i in range(0,3):
      if Zi[i].size > 0:
        fig = plt.figure()
        if not(np.nanmax(Zi[i]) == 0 and np.nanmin(Zi[i]) == 0):
          CS = plt.contour(xi,yi,Zi[i],15,linewidths=0.5,colors='k')
          CS = plt.contourf(xi,yi,Zi[i],15,cmap=plt.cm.jet)
          plt.colorbar()
        if i < 2:
          plt.scatter(X[i],Y[i],marker='o',c='b',s=5)
        plt.xlim(plotx[0],plotx[1])
        plt.ylim(ploty[0],ploty[1])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        sio = cStringIO.StringIO()
        fig.savefig(sio,format="png")
        string = sio.getvalue() 
        ret.append(string.encode("base64").strip())
      else:
        ret.append("")
    
    return Response(dumps(ret))
  
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

