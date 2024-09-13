import os
import boto3
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client('s3')

S3_BUCKET = os.getenv('S3_BUCKET')
MODEL_KEY = os.getenv('MODEL_KEY')
VERSION_KEY = os.getenv('VERSION_KEY')
LOCAL_MODEL_PATH = os.getenv('LOCAL_MODEL_PATH')
LOCAL_VERSION_PATH = os.getenv('LOCAL_VERSION_PATH')

def get_model_version_from_s3():
    try:
        response = s3.get_object(Bucket=S3_BUCKET, Key=VERSION_KEY)
        return response['Body'].read().decode('utf-8').strip()
    except Exception as e:
        print(f'Error while fetching model version from S3: {e}')


def get_local_model_version():
    if os.path.exists(LOCAL_VERSION_PATH):
        with open(LOCAL_VERSION_PATH, 'r') as file:
            return file.read().strip()

    return None

def download_model_from_s3():
    # Ensure the local directory exists
    if not os.path.exists(LOCAL_MODEL_PATH):
        os.makedirs(LOCAL_MODEL_PATH)

    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=MODEL_KEY)

    if 'Contents' in response:
        for obj in response['Contents']:
            file_key = obj['Key']
            # Remove the prefix from the key to get the local file path
            relative_path = os.path.relpath(file_key, MODEL_KEY)
            local_file_path = os.path.join(LOCAL_MODEL_PATH, relative_path)

            print(f"Downloading {file_key} to {local_file_path}...")

            # Download the file
            s3.download_file(S3_BUCKET, file_key, local_file_path)

    else:
        print(f"No contents found under prefix {MODEL_KEY}")


def is_model_outdated():
    s3_version = get_model_version_from_s3()
    local_version = get_local_model_version()
    return s3_version != local_version

def check_and_download_model():
    if is_model_outdated() or not os.path.exists(LOCAL_MODEL_PATH):
        print("Model is outdated or missing, downloading new version...")
        download_model_from_s3()