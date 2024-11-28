import os
import time
from kafka import KafkaProducer
from faker import Faker
import json

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 5))

fake = Faker()

def get_faker_data():
    return {
        "name": fake.name(),
        "ssn": fake.ssn(),
        "job": fake.job(),
        "year": fake.year(),
        "company": fake.company(),
        "company_email": fake.company_email(),
        "building_number": fake.building_number(),
        "street_name": fake.street_name(),
        "city": fake.city(),
        "country": fake.country(),
        "postcode": fake.postcode(),
        "passport_number": fake.passport_number(),
        "credit_card_provider": fake.credit_card_provider(),
        "credit_card_number": fake.credit_card_number(),
        "credit_card_expire": fake.credit_card_expire(),
        "credit_card_security_code": fake.credit_card_security_code()
    }

def run():
    iterator = 0
    print("Setting up Faker producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    while True:
        sendit = get_faker_data()
        print("Sending new faker data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=sendit)
        print("New faker data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1


if __name__ == "__main__":
    run()