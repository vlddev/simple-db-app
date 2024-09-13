# build with "docker build --rm -t simple-py-web-app ."
FROM python:3.10-alpine AS build

RUN apk add build-base libpq libpq-dev

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine AS final

RUN apk update \
    && apk upgrade \
    && apk add --no-cache libpq 

WORKDIR /app/

COPY ./ ./
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

#RUN pip install --upgrade pip

#COPY ./requirements.txt /app/requirements.txt

# install dependencies
#RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY static static/
COPY templates templates/
COPY *.py ./

# command to run on container start
CMD ["python", "./server.py"]
