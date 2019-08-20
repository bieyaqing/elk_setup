# ELK Setup

## Docker link:
https://elk-docker.readthedocs.io/

## Docker compose
```yml
ubuntu:
  image: ubuntu
  stdin_open: true
  tty: true

elk:
  image: sebp/elk
  ports:
    - "5601:5601"
    - "9200:9200"
    - "5044:5044"
```
### Command
```
docker-compose up elk
docker-compose up ubuntu
```