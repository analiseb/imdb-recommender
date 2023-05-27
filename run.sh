#! /bin/bash
docker stop movie_website
docker rm movie_website
docker run -i -t -e PORT=8000 -p 8000:8000 --name movie_website movie_website
