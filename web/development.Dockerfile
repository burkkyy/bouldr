FROM node:23.2.0-alpine3.20

WORKDIR /usr/src/web

COPY package*.json ./

RUN npm install

COPY . .

CMD ["npm", "run", "start"]
