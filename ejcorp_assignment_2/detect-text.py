import boto3

client = boto3.client('rekognition')

response = client.detect_text(
    Image={
        'S3Object': {
            'Bucket': 'info7374-image-detection',
            'Name': 'Raw/product-500x500.jpeg'
        }
    }
)

print(response)
print(response['TextDetections'][0]['DetectedText'])