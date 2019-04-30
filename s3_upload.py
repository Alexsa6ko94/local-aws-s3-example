import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Init the boto3 client    
    s3_client = boto3.client(
        service_name='s3',
	aws_access_key_id='123',
	aws_secret_access_key='xyz',
	endpoint_url='http://localhost:4572',
    )

    # Url to the uploaded file
    object_url = '{endpoint_url}/{bucket_name}/{file_name}'.format(
        endpoint_url=s3_client.meta.endpoint_url,
        bucket_name=bucket,
        file_name=file_name
    )

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print('Object URL: {}'.format(object_url))
    except ClientError as e:
        logging.error(e)
        return False
    return True


if __name__ == "__main__":
    upload_file('test-upload.jpg', 'demo-bucket')

