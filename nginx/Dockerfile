FROM nginx:latest
COPY ./static/ /usr/share/nginx/source
COPY ./nginx/conf/instagraph.conf /etc/nginx/conf.d
RUN rm ./etc/nginx/conf.d/default.conf

###### ----- this commands are assumed to be executed inside the parent directory
###### ----- e.g  docker build -f ./nginx/Dockerfile -t enginex .