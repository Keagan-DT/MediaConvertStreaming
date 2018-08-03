import boto3
import ast
import urllib2

mc = boto3.client('mediaconvert',endpoint_url='https://jxtpe23s.mediaconvert.eu-west-1.amazonaws.com')
s3 = boto3.client('s3')


def createJob(bucket, fileKey):
    response = mc.create_job(
        JobTemplate='Converter0.01',
        Queue='arn:aws:mediaconvert:eu-west-1:083435387476:queues/Default',
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
    return response

def getKeyName(event):
    key = event['Records'][0]['s3']['object']['key']
    urllib2.unquote(key)
    return key
 
def getBucketName(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    return bucket 
   
def main():
    file = open("/home/ec2-user/environment/ConvertHandeling/exampleEvent.json", "r") 
    f = file.read()
    event = ast.literal_eval(f)
    key = getKeyName(event)
    bucket =  getBucketName(event)
    
    print(bucket + " " + key)
    
    #createJob( bucket, key)
    
if __name__=='__main__':
    main()