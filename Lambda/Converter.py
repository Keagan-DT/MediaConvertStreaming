import boto3
from urllib.parse import unquote
import threading
from threading import Thread

mc = boto3.client('mediaconvert',endpoint_url='https://jxtpe23s.mediaconvert.eu-west-1.amazonaws.com')
sns = boto3.client('sns')
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote(event['Records'][0]['s3']['object']['key']).replace('+', ' ')
    
    Thread(target = convert(bucket, key, 'HLS')).start()
    Thread(target = convert(bucket, key, 'DASH')).start()
    Thread(target = convert(bucket, key, 'FILE')).start()

def convert(bucket,fileKey, outType):
    response = mc.create_job(
        JobTemplate = outType + 'converter',
        Queue='arn:aws:mediaconvert:eu-west-1:083435387476:queues/' + outType + 'queue',
        Role='arn:aws:iam::083435387476:role/MediaConvert',
        Settings={
            'AdAvailOffset': 0,
            'Inputs': [
                {
                    'AudioSelectors': {
                        'Audio Selector 1': {
                            'DefaultSelection': 'DEFAULT',
                            'Offset': 0,
                            'ProgramSelection': 1,
                        }
                    },
                    'DeblockFilter': 'DISABLED',
                    'DenoiseFilter': 'DISABLED',
                    'FileInput': "s3://"+ str(bucket) +"/" + str(fileKey),
                    'FilterEnable': 'AUTO',
                    'FilterStrength': 0,
                    'PsiControl': 'USE_PSI',
                    'TimecodeSource': 'EMBEDDED',
                    'VideoSelector': {
                    'ColorSpace': 'FOLLOW'
                    }
                }
            ]
        }
    )
    
def sendNoti(key):
    response = sns.publish(
        TopicArn='arn:aws:sns:eu-west-1:083435387476:New_Convert_Job_Started',
        Message=key + ' Started to be converted',
        Subject='New Convert Job Started',
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'UTF8 '
            }
        }
    )
    
    