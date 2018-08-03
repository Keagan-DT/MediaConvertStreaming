import boto3
import time

mc = boto3.client('mediaconvert',endpoint_url='https://jxtpe23s.mediaconvert.eu-west-1.amazonaws.com')

def getJobStatus(status, x):
    response = mc.list_jobs(
        MaxResults=x,
        Order='DESCENDING',
        Queue='arn:aws:mediaconvert:eu-west-1:083435387476:queues/Default',
        Status=status
    )
    return response['Jobs']
    

def main():
   checkingJob = getJobStatus("PROGRESSING",1)
   tenpJob = checkingJob
   x=0
   if checkingJob != '[]':
        while tenpJob == checkingJob:
            print(str(checkingJob[0]['Settings']['Inputs'][0]['FileInput']) + " is still progressing, checking in 30s")
            time.sleep(30)
            tenpJob = getJobStatus("PROGRESSING",1)
            x+=1
   if x > 0:
       print(str(checkingJob[0]['Settings']['Inputs'][0]['FileInput']) + " Compleed")
   else:
       print("No Jobs Progressing")
        

if __name__=='__main__':
    main()