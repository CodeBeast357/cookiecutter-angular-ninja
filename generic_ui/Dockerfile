FROM node:18 as build

RUN npm install
RUN npm install -g @angular/cli

WORKDIR /app
COPY generic_app /app

RUN ng build --output-path=dist --base-href=/ui/

FROM nginx:1.16.0-alpine

COPY --from=build /app/dist /usr/share/nginx/html/ui
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
