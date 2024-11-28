#!/bin/sh

# OpenWeather Sink
echo "Starting Weather Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "weathersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "weather",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.weather.kafkapipeline.weatherreport.mapping": "location=value.location, forecastdate=value.report_time, description=value.description, temp=value.temp, feels_like=value.feels_like, temp_min=value.temp_min, temp_max=value.temp_max, pressure=value.pressure, humidity=value.humidity, wind=value.wind, sunrise=value.sunrise, sunset=value.sunset",
    "topic.weather.kafkapipeline.weatherreport.consistencyLevel": "LOCAL_QUORUM"
  }
}'

# FakerAPI Sink
echo "Starting Faker Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "fakersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "faker",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.faker.kafkapipeline.fakerdata.mapping": "name=value.name, ssn=value.ssn, job=value.job, year=value.year, company=value.company, company_email=value.company_email, building_number=value.building_number, street_name=value.street_name, city=value.city, country=value.country, postcode=value.postcode, passport_number=value.passport_number, credit_card_provider=value.credit_card_provider, credit_card_number=value.credit_card_number, credit_card_expire=value.credit_card_expire, credit_card_security_code=value.credit_card_security_code",
    "topic.faker.kafkapipeline.fakerdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'

# TMDB API Sink
echo "Starting TMDB Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "tmdbsink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable": "false",
    "tasks.max": "10",
    "topics": "tmdb",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.tmdb.kafkapipeline.movies.mapping": "id=value.id, title=value.title, original_title=value.original_title, overview=value.overview, original_language=value.original_language, adult=value.adult, popularity=value.popularity, vote_average=value.vote_average, vote_count=value.vote_count, release_date=value.release_date",
    "topic.tmdb.kafkapipeline.movies.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."