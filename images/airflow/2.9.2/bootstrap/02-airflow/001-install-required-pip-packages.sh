#!/bin/bash
set -e

# shellcheck source=images/airflow/2.9.2/bootstrap/common.sh
source /bootstrap/common.sh

# Define an array of required packages
REQUIRED_PACKAGES=(
    "apache-airflow-providers-amazon[aiobotocore]"
    "apache-airflow[celery,statsd]==${AIRFLOW_VERSION}"
    "celery[sqs]"
    "boto3-stubs[logs]"
    "boto3-stubs[sqs]"
    psycopg2
    pycurl
    watchtower
)

# safe-pip-install always install all required packages, along with whatever
# the user provides, hence we don't need to provide anything here.
safe-pip-install "${REQUIRED_PACKAGES[@]}" 
