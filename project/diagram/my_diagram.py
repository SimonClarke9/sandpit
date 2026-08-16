from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.custom import Custom

with Diagram("kafka_to_lambda_raw_eventbridge_iceberg_staging", filename="pipeline_diagram", show=False, graph_attr={"rankdir": "TB"}):

    # Data sources
    json_file = Custom("JSON File", "./icons/json.png")
    csv_file = Custom("CSV File", "./icons/csv.png")

    # Kafka
    kafka = Kafka("Kafka Service")

    # Lambda
    lambda_fn = Lambda("Topic: Save Raw Data")

    # S3 Buckets
    raw_bucket = S3("S3 Bucket: RAW")
    staging_bucket = S3("S3 Iceberg Bucket: STAGING")

    # EventBridge
    event_bridge = Eventbridge("EventBridge Trigger: new File event")

    # Flow
    json_file >> kafka
    csv_file >> kafka

    kafka >> lambda_fn >> raw_bucket

    raw_bucket >> event_bridge >> staging_bucket
