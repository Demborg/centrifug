# Centrifug
Interactive video selection for my upcomming exhibtion

## Backend
Build the dockerized backend as:
`docker build . --tag demborg/centrifug`

And push to dockerhub as:
`docker push demborg/centrifug:latest`

## Frontend
To server the video viewer frontend on local port 8000:
`cd frontend`
`python3 -m http.server 8000`