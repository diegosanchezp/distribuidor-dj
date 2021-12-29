FROM node:17 AS jsbuild
WORKDIR /distribuidor-dj
COPY django/ .
RUN cd ./django/distribuidor_dj/apps/tailwind_theme/static_src && \
    # Install nodejs dependencies
    npm ci --only=production && \
    # Build tailwind CSS
    npm run build

FROM python:3.9.9
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /distribuidor-dj
COPY --from=jsbuild /distribuidor-dj .
RUN pip install -r requirements.txt
RUN ./django/manage.py migrate && \
    ./django/manage.py collectstatic --noinput
# TODO:Run the image as a non-root user
# RUN adduser -D myuser
# USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD gunicorn --chdir ./django --bind 0.0.0.0:$PORT distribuidor_dj.wsgi
