import os
import urlparse


import flask
from flask import Response
from flask import request

app = flask.Flask(__name__)


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.interpolate import griddata
import urllib
import numpy.ma as ma
import cStringIO

#import time

from simplejson import loads,dumps
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin','*')
  return response

@app.route("/floorviewer/generate",methods=['POST'])
def on_generate_png():
    print 'hello'
    thing = request.form
    #print thing.items()[0][0]
    d = loads(thing.items()[0][0])
    
    #print d
    ret = [] #returns three png things
    X = [];
    Y = [];
    Z = [];
    Zi = [];
    plotx = [float("Inf"),float("-Inf")]
    ploty = [float("Inf"),float("-Inf")]
    plotz = [float("Inf"),float("-Inf")]
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

        plotz[0] = min(plotz[0],np.nanmin(Zi[i]));
        plotz[1] = max(plotz[1],np.nanmax(Zi[i]));

      else:
        Zi.append(np.array([]))

    if Zi[0].size > 0 and Zi[1].size > 0:
      Zi.append(np.subtract(Zi[1],Zi[0]))
    else:
      Zi.append(np.array([]))

    for i in range(0,3):
      if Zi[i].size > 0:
        fig = plt.figure()
        #time_start = time.time()
        if not(np.nanmax(Zi[i]) == np.nanmin(Zi[i])):
          if i < 2:
            clevels = np.linspace(plotz[0],plotz[1],15)
          else:
            clevels = 15
          CS = plt.contour(xi,yi,Zi[i],clevels,linewidths=0.5,colors='k')
          CS = plt.contourf(xi,yi,Zi[i],clevels,cmap=plt.cm.jet)
          plt.colorbar()
        if i < 2:
          plt.scatter(X[i],Y[i],marker='o',c='b',s=5)
        plt.xlim(plotx[0],plotx[1])
        plt.ylim(ploty[0],ploty[1])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.show()
        #time_elapsed = time.time() - time_start
        #fig.suptitle(str(time_elapsed))
        sio = cStringIO.StringIO()
        fig.savefig(sio,format="png")
        string = sio.getvalue() 
        ret.append(string.encode("base64").strip())
        plt.close()
      else:
        ret.append("")

    r = Response(dumps(ret))
    
    return r
  

if __name__ == '__main__':
  app.run(host="0.0.0.0",port=5000,debug=True)
