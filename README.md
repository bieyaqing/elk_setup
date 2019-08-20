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
### Commands
```
docker-compose up elk
docker-compose up ubuntu
```

## Logstash Config
```conf
filter {
  if [type] == "log" {
    grok {
      match => { "message" => "\[%{WORD:level}\]\[%{IP:ipaddr}\]\[%{TIMESTAMP:timestamp}\] %{GREEDYDATA:message}" }
    }
  }
}
```
### Link
https://github.com/elastic/logstash/blob/v1.4.2/patterns/grok-patterns
