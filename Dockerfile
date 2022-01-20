FROM ghcr.io/diegosanchezp/distribuidor-dj:latest

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --chdir ./django --bind 0.0.0.0:$PORT distribuidor_dj.wsgi
