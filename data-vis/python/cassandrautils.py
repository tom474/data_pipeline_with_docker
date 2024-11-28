import os
import sys

import pandas as pd
from cassandra.cluster import BatchStatement, Cluster, ConsistencyLevel
from cassandra.query import dict_factory

tablename = os.getenv("weather.table", "weatherreport")
fakertable = os.getenv("faker.table", "fakerdata")
tmdbtable = os.getenv("tmdb.table", "movies")

CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST") if os.environ.get("CASSANDRA_HOST") else 'localhost'
CASSANDRA_KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE") if os.environ.get("CASSANDRA_KEYSPACE") else 'kafkapipeline'

WEATHER_TABLE = os.environ.get("WEATHER_TABLE") if os.environ.get("WEATHER_TABLE") else 'weather'
FAKER_TABLE = os.environ.get("FAKER_TABLE") if os.environ.get("FAKER_TABLE") else 'faker'
TMDB_TABLE = os.environ.get("TMDB_TABLE") if os.environ.get("TMDB_TABLE") else 'tmdb'


def saveWeatherreport(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + tablename + " (forecastdate, location, description, temp, feels_like, temp_min, temp_max, pressure, humidity, wind, sunrise, sunset) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (val['report_time'], val['location'], val['description'],
                           val['temp'], val['feels_like'], val['temp_min'], val['temp_max'],
                           val['pressure'], val['humidity'], val['wind'], val['sunrise'], val['sunset']))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')


def saveFakerDf(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + fakertable + " (name, ssn, job, year, company, company_email, building_number, street_name, city, country, postcode, passport_number, credit_card_provider, credit_card_number, credit_card_expire, credit_card_security_code) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (
            val['name'], val['ssn'], val['job'], val['year'],
            val['company'], val['company_email'], val['building_number'],
            val['street_name'], val['city'], val['country'], val['postcode'],
            val['passport_number'], val['credit_card_provider'],
            val['credit_card_number'], val['credit_card_expire'],
            val['credit_card_security_code']
        ))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')


def saveMoviesDf(dfrecords):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    session = cluster.connect(CASSANDRA_KEYSPACE)

    counter = 0
    totalcount = 0

    cqlsentence = "INSERT INTO " + tmdbtable + " (id, title, original_title, overview, original_language, adult, popularity, vote_average, vote_count, release_date) \
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    insert = session.prepare(cqlsentence)
    batches = []
    for idx, val in dfrecords.iterrows():
        batch.add(insert, (
            val['id'], val['title'], val['original_title'], val['overview'],
            val['original_language'], val['adult'], val['popularity'],
            val['vote_average'], val['vote_count'], val['release_date'],
        ))
        counter += 1
        if counter >= 100:
            print('inserting ' + str(counter) + ' records')
            totalcount += counter
            counter = 0
            batches.append(batch)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
    if counter != 0:
        batches.append(batch)
        totalcount += counter
    rs = [session.execute(b, trace=True) for b in batches]

    print('Inserted ' + str(totalcount) + ' rows in total')


def loadDF(targetfile, target):
    if target == 'weather':
        colsnames = ['description', 'temp', 'feels_like', 'temp_min', 'temp_max',
                     'pressure', 'humidity', 'wind', 'sunrise', 'sunset', 'location', 'report_time']
        dfData = pd.read_csv(targetfile, header=None, parse_dates=True, names=colsnames)
        dfData['report_time'] = pd.to_datetime(dfData['report_time'])
        saveWeatherreport(dfData)
    elif target == 'faker':
        colsnames = ['name', 'ssn', 'job', 'year', 'company', 'company_email', 'building_number',
                     'street_name', 'city', 'country', 'postcode', 'passport_number',
                     'credit_card_provider', 'credit_card_number', 'credit_card_expire',
                     'credit_card_security_code']
        dfData = pd.read_csv(targetfile, header=None, names=colsnames)
        saveFakerDf(dfData)
    elif target == 'tmdb':
        colsnames = ['id', 'title', 'original_title', 'overview', 'original_language',
                     'adult', 'popularity', 'vote_average', 'vote_count', 'release_date']
        dfData = pd.read_csv(targetfile, header=None, names=colsnames)
        saveMoviesDf(dfData)
    else:
        print(f"Unsupported target: {target}")


def getWeatherDF():
    return getDF(WEATHER_TABLE)
def getFakerDF():
    print(FAKER_TABLE)
    return getDF(FAKER_TABLE)
def getMoviesDF():
    print(TMDB_TABLE)
    return getDF(TMDB_TABLE)

def getDF(source_table):
    if isinstance(CASSANDRA_HOST, list):
        cluster = Cluster(CASSANDRA_HOST)
    else:
        cluster = Cluster([CASSANDRA_HOST])

    if source_table not in (WEATHER_TABLE, FAKER_TABLE, TMDB_TABLE):
        return None

    session = cluster.connect(CASSANDRA_KEYSPACE)
    session.row_factory = dict_factory
    cqlquery = "SELECT * FROM " + source_table + ";"
    rows = session.execute(cqlquery)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    action = sys.argv[1]
    target = sys.argv[2]
    targetfile = sys.argv[3]
    if action == "save":
        loadDF(targetfile, target)
    elif action == "get":
        getDF(target)
