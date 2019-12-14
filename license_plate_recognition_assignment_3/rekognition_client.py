import boto3


def detectText(bucket, key):
    # Change the value of bucket to the S3 bucket that contains your image file.
    # Change the value of photo to your image file name.
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': key}})
    text_detections = response['TextDetections']
    print('Detected text')
    for text in text_detections:
        print('Detected text:' + text['DetectedText'])
        print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print('Parent Id: {}'.format(text['ParentId']))
        print('Type:' + text['Type'])
        # print
        return ('Detected text:' + text['DetectedText'])

detectText('info7374-image-detection','DVLA-number-plates-2017-67-new-car-847566.jpg')
