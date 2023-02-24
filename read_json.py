import boto3
import json
from botocore.config import Config
import datetime
import pg8000

# Connect to the database
conn = pg8000.connect(
    host="localhost",
    user="postgres",
    password="postgres"
)

cur = conn.cursor()
# Change app_version type as it is format Integer in DDL but actual values are of *.*.*.* type
cur.execute("""ALTER TABLE user_logins ALTER COLUMN app_version TYPE varchar (20);""")


# Configure boto3 to use localstack
endpoint_url = 'http://localhost:4566'
region_name = 'us-east-1'
# Create a SQS client
config = Config(
    retries=dict(
        max_attempts=10
    ),
    region_name=region_name,
    signature_version='v4',
   
)

sqs = boto3.client('sqs', endpoint_url=endpoint_url, config=config,aws_access_key_id='test', aws_secret_access_key='test')

# Retrieve messages from the queue
response = sqs.receive_message(
    QueueUrl='http://localhost:4566/000000000000/login-queue',
    AttributeNames=['All'],
    MessageAttributeNames=['All'],
    MaxNumberOfMessages=5
)
# Process each message
for message in response['Messages']:
    # Extract the JSON data from the message body
    message_body = json.loads(message['Body'])
    # Process the JSON data as needed
    masked_message_body = {
        'user_id': message_body['user_id'],
        'app_version': message_body['app_version'],
        'device_type': message_body['device_type'],
        'masked_ip': '{}'.format(hash(message_body['ip'])),
        'locale': message_body['locale'],
        'masked_device_id': '{}'.format(hash(message_body['device_id'])),
        'create_date': datetime.date.today()

                            }
    print(type(masked_message_body['create_date']))
    print(masked_message_body)
    # Insert data into the table
    cur.execute("""INSERT INTO user_logins (user_id, app_version,device_type,masked_ip,locale,masked_device_id,create_date) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}');""".format(masked_message_body['user_id'], masked_message_body['app_version'], masked_message_body['device_type'], masked_message_body['masked_ip'], masked_message_body['locale'], masked_message_body['masked_device_id'],masked_message_body['create_date']))

# Commit changes to the database
    conn.commit()
    # Delete the message from the queue
    sqs.delete_message(
        QueueUrl='http://localhost:4566/000000000000/login-queue',
        ReceiptHandle=message['ReceiptHandle']
    )


# Close the cursor and connection
cur.close()
conn.close()
