#ベースイメージの指定
FROM node:lts-slim
#作業ディレクトリを/src/webに設定
# WORKDIR /src/web
WORKDIR /app
COPY package*.json ./
COPY taskapp-web/package.json taskapp-web/package-lock.json* ./

RUN npm install -g npm
RUN npm install -g vue-cli

# RUN npm init -y


RUN npm install

COPY . .

EXPOSE 5173
CMD [ "npm","run","dev","--","--host","0.0.0.0"]