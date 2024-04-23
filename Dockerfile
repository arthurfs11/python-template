FROM python:3.11.0-bullseye

# Fix timezone container
ENV TZ=America/Sao_Paulo
ENV TERM=xterm
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


# UPDATE APT-GET
RUN apt-get update

RUN apt-get install nano -y

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
