USE kafkapipeline;

CREATE TABLE IF NOT EXISTS kafkapipeline.weatherreport (
  forecastdate TIMESTAMP,
  location TEXT,
  description TEXT,
  temp FLOAT,
  feels_like FLOAT,
  temp_min FLOAT,
  temp_max FLOAT,
  pressure FLOAT,
  humidity FLOAT,
  wind FLOAT,
  sunrise BIGINT,
  sunset BIGINT,
  PRIMARY KEY (location, forecastdate)
);

CREATE TABLE IF NOT EXISTS kafkapipeline.fakerdata (
  name TEXT,
  ssn TEXT,
  job TEXT,
  year INT,
  company TEXT,
  company_email TEXT,
  building_number TEXT,
  street_name TEXT,
  city TEXT,
  country TEXT,
  postcode TEXT,
  passport_number TEXT,
  credit_card_provider TEXT,
  credit_card_number TEXT,
  credit_card_expire TEXT,
  credit_card_security_code TEXT,
  PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS kafkapipeline.movies (
  id INT,
  title TEXT,
  original_title TEXT,
  overview TEXT,
  original_language TEXT,
  adult BOOLEAN,
  popularity TEXT,
  vote_average FLOAT,
  vote_count INT,
  release_date TEXT,
  PRIMARY KEY (id)
);
