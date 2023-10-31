FROM node:18

RUN mkdir /src
WORKDIR /src

ADD package.json /src/package.json

RUN npm install

COPY . /src

EXPOSE 6000

CMD npm start