# ETL-off-a-SQS-Queue

Objective :

1. read JSON data containing user login behavior from an AWS SQS Queue, that is made
available via a custom localstack image that has the data pre loaded.
2. Fetch wants to hide personal identifiable information (PII). The fields `device_id` and `ip`
should be masked, but in a way where it is easy for data analysts to identify duplicate
values in those fields.
3. Once you have flattened the JSON data object and masked those two fields, write each
record to a Postgres database that is made available via a custom postgres image that
has the tables pre created.

Approach:

To read messages from the queue, I use the boto3 library to connect to the SQS queue and fetch messages.
For masking the device_id and ip fields, I have used hashing to mask the original value. This will allow us to maintain the ability to identify duplicate values without revealing the actual value.
To connect and write to Postgres,I have used the pg8000 library to connect to the database and execute SQL queries.  

- To deploy this application in production, we can use container orchestration tools like Kubernetes to manage the containers and scale the application.Addition of cloud provider like AWS or GCP to host the containers and manage the infrastructure.
- To make this production-ready, we can add monitoring and logging solutions like Splunk to monitor the application's performance and logs. We can also add load balancers and auto-scaling policies to handle high traffic and sudden spikes in the workload.
- To scale this application with a growing dataset, we can use sharding and partitioning techniques to distribute the data across multiple database instances. We can also use data warehousing solutions like BigQuery to store and analyze large datasets or use Hadoop/PySpark Tech Stack.
- To recover PII later on, we can use a secure key management system to store the keys used to mask the data. We can also implement access control policies to restrict access to the PII data.

Assumptions:

The JSON data is in a flat format and does not contain nested objects or arrays.
The device_id and ip fields are unique and not null.
The Postgres database has enough capacity to handle the incoming data.
Next steps:

Implement a solution to handle batch processing of messages from the SQS queue.
Add unit tests and integration tests to ensure the application's correctness.
Use a container registry like AWS ECR to store the container images.
Implement an API to expose the data stored in the Postgres database.
Use a continuous integration and deployment tool to automate the deployment process.
