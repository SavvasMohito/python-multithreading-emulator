FROM node:16-stretch
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN npm install -g npm@7.11.1

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

ENV NODE_ENV=production
COPY ["package.json", "package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production && mv node_modules ../
EXPOSE 3333

CMD ["/init"]