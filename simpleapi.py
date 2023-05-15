from flask import Flask , request
import requests
import json

app         = Flask( __name__ )
API_KEY     = "b6907d289e10d714a6e88b30761fae22"
description = """
   <!DOCTYPE html>
   <head>
   <title>API Landing</title>
   </head>
   <body>  
      <h4>A simple API using Flask</h4>
      <a href="/square?value=2">Request Sample: Square</a>
      </br>
      <a href="/london/uk">Request Sample: Weather</a>
   </body>
   """
#

@app.route('/')
def index():
   #
   #return 'App Work !!!'
   return description
#

@app.route( '/<string:city>/<string:country>' )
def weather_by_city( country , city ):
   #
   url = 'https://samples.openweathermap.org/data/2.5/weather'
   params = dict (
      q     = city + "," + country ,
      appid = API_KEY ,
   )  #
   response = requests.get( url = url , params = params )
   data     = response.json()
   return data
#

@app.route( '/square' , methods = [ 'GET' ] )
def square():
   #
   if not all( k in request.args for k in ( [ "value" ] ) ):
      error_message = f"\
         Required parameters : 'value'<br>\
         Supplied parameters : { [ k for k in request.args ] } \
         "
      return error_message
   else:
      value = int( request.args[ 'value' ] )
      return json.dumps({"Value Squared" : value**2})
#

def main():
   #
   app.run( host = "0.0.0.0", port = 5000 )
#

if __name__ == '__main__':
   main()
#