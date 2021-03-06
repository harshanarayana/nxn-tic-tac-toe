# Fetch the Base container Image with 3.6.5
FROM python:3.6.5-alpine3.6

LABEL maintainer="harsha2k4@gmail.com"

# Copy Game Stuff to Container
COPY ttt /game/ttt
COPY utils /game/utils
COPY setup.py /game
COPY tic-tac-toe.py /game
COPY requirements.txt /game
COPY README.md /game
COPY tic-tac-toe /usr/local/bin
COPY tic-tac-toe /game

# Install Python dependencies and module.
RUN apk add --update bash && rm -rf /var/cache/apk/*
WORKDIR /game
RUN pip install -r requirements.txt && pip install -e .
RUN echo 'alias tic-tac-toe="python /game/tic-tac-toe.py"' >> ~/.bashrc

# Setup Path Variables
RUN export PATH=$PATH:/game

CMD ["tic-tac-toe"]