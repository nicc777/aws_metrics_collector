import boto3
import traceback
from aws_metrics_collector import LogWrapper


INSTANCE_CLASSES = (
    'EC2',
    'RDS',
)


class AwsInstance:

    def __init__(self, instance_class: str='EC2'):
        self.instance_class = instance_class


class AwsEC2Instance(AwsInstance):

    def __init__(self):
        super().__init__(instance_class='EC2')


def get_ec2_instances(aws_client, next_token: str=None, log_wrapper=LogWrapper())->list:
    '''Using boto3, get the list of EC2 instances and create a AwsEC2Instance 
    instance of each, storing the collection in a result which is then returned.
    '''
    result = list()
    try:
        if next_token is not None:
            response = aws_client.describe_instances(
                MaxResults=20,
                NextToken=next_token
            )
        else:
            response = aws_client.describe_instances(
                MaxResults=20,
                NextToken=next_token
            )
        if 'NextToken' in result:
            if isinstance(response['NextToken'], str):
                if len(response['NextToken']) > 0:
                    next_result = get_ec2_instances(aws_client=aws_client, next_token=response['NextToken'], log_wrapper=log_wrapper)
                    result = result + next_result
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return result


# EOF 
