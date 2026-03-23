import boto3

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')

SNS_TOPIC_ARN = 'YOUR_SNS_TOPIC_ARN'
INSTANCE_AMI = 'ami-xxxxxxxx'  # Replace
INSTANCE_TYPE = 't2.micro'

def lambda_handler(event, context):
    # Get average CPU utilization (last 5 mins)
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        StartTime=datetime.utcnow() - timedelta(minutes=5),
        EndTime=datetime.utcnow(),
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']
    
    if not datapoints:
        return "No data"

    cpu = datapoints[0]['Average']

    if cpu > 80:
        # Scale up
        instance = ec2.run_instances(
            ImageId=INSTANCE_AMI,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE
        )

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f"Scaling UP - CPU: {cpu}"
        )

    elif cpu < 20:
        # Scale down
        instances = ec2.describe_instances()
        instance_ids = [i['InstanceId'] for r in instances['Reservations'] for i in r['Instances']]

        if len(instance_ids) > 1:
            ec2.terminate_instances(InstanceIds=[instance_ids[-1]])

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message=f"Scaling DOWN - CPU: {cpu}"
            )

    return f"CPU Utilization: {cpu}"
