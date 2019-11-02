import boto3
import traceback
from datetime import datetime
from aws_metrics_collector import LogWrapper
from aws_metrics_collector import get_utc_timestamp


INSTANCE_CLASSES = (
    'ec2',
    'rds',
)
MAX_RESULTS_DEFAULT = 20


class AwsInstance:

    def __init__(self, instance_class: str='ec2', log_wrapper: LogWrapper=LogWrapper()):
        self.instance_class = instance_class
        self.log_wrapper = log_wrapper
        self.last_update = None
        self.raw_instance_data = None

    def store_raw_instance_data(self, instance_data: dict):
        if instance_data is not None:
            if isinstance(instance_data, dict):
                self.raw_instance_data = instance_data
                self.last_update = get_utc_timestamp(with_decimal=False)
        self._post_store_raw_instance_data_processing()

    def _post_store_raw_instance_data_processing(self):
        pass


class AwsEC2Instance(AwsInstance):

    def __init__(self, log_wrapper: LogWrapper=LogWrapper()):
        self.instance_id = 'unknown'
        self.instance_type = 'unknown'
        self.state = 'stopped'
        super().__init__(instance_class='ec2', log_wrapper=log_wrapper)

    def _post_store_raw_instance_data_processing(self):
        self.log_wrapper.info(message='Processing a ec2 result')
        if self.raw_instance_data is not None:
            if 'InstanceId' in self.raw_instance_data:
                self.instance_id = self.raw_instance_data['InstanceId']
            if 'InstanceType' in self.raw_instance_data:
                self.instance_type = self.raw_instance_data['InstanceType']
            if 'State' in self.raw_instance_data:
                if 'Name' in self.raw_instance_data['State']:
                    self.state = self.raw_instance_data['State']['Name']
            self.log_wrapper.info(message='Processed instance ID "{}"'.format(self.instance_id))
        else:
            self.log_wrapper.error(message='raw_instance_data is None')


class AwsRDSInstance(AwsInstance):

    def __init__(self, log_wrapper: LogWrapper=LogWrapper()):
        super().__init__(instance_class='ec2', log_wrapper=log_wrapper)

    def _post_store_raw_instance_data_processing(self):
        self.log_wrapper.info(message='Processing a ec2 result')
        if self.raw_instance_data is not None:
            self.log_wrapper.info(message='Processed RDS Instance')


class AWSInstanceCollection:

    def __init__(self, log_wrapper: LogWrapper=LogWrapper()):
        self.instances = list()
        self.log_wrapper = log_wrapper


def get_regions_by_service(service='ec2', log_wrapper=LogWrapper())->list:
    try:
        return list(boto3.session.Session().get_available_regions(service))
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return ['us-east-1']


def get_ec2_instances(
    aws_client, 
    next_token: str=None, 
    max_results_per_iteration: int=MAX_RESULTS_DEFAULT, 
    log_wrapper=LogWrapper()
)->list:
    '''Using boto3, get the list of EC2 instances and create a AwsEC2Instance 
    instance of each, storing the collection in a result which is then returned.
    '''
    result = list()
    if aws_client is not None:
        try:
            if next_token is not None:
                response = aws_client.describe_instances(
                    MaxResults=max_results_per_iteration,
                    NextToken=next_token
                )
            else:
                response = aws_client.describe_instances(
                    MaxResults=max_results_per_iteration
                )
            ### Main processing ###

            if 'Reservations' in response:
                for reservation in response['Reservations']:
                    if 'Instances' in reservation:
                        for instance_data in reservation['Instances']:
                            ec2instance = AwsEC2Instance(log_wrapper=log_wrapper)
                            ec2instance.store_raw_instance_data(instance_data=instance_data)
                            if ec2instance.raw_instance_data is not None:
                                result.append(ec2instance)

            ### end main processing ###
            if 'NextToken' in response:
                if isinstance(response['NextToken'], str):
                    if len(response['NextToken']) > 0:
                        next_result = get_ec2_instances(
                            aws_client=aws_client, 
                            next_token=response['NextToken'], 
                            max_results_per_iteration=max_results_per_iteration, 
                            log_wrapper=log_wrapper
                        )
                        result = result + next_result
        except:
            log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    else:
        log_wrapper.warning(message='No EC2 instances were fetched because the aws_client was not defined - failing gracefully...')
    return result


def get_rds_instances(
    aws_client, 
    next_token: str=None, 
    max_results_per_iteration: int=MAX_RESULTS_DEFAULT, 
    log_wrapper=LogWrapper()
)->list:
    '''Using boto3, get the list of RDS instances and create a AwsRDSInstance 
    instance of each, storing the collection in a result which is then returned.
    '''
    result = list()
    if aws_client is not None:
        try:
            if next_token is not None:
                response = aws_client.describe_db_instances(
                    MaxRecords=max_results_per_iteration,
                    Marker=next_token
                )
            else:
                response = aws_client.describe_db_instances(
                    MaxRecords=max_results_per_iteration
                )
            ### Main processing ###

            if 'DBInstances' in response:
                for db_instance_data in response['DBInstances']:
                    rds_instance = AwsRDSInstance(log_wrapper=log_wrapper)
                    rds_instance.store_raw_instance_data(instance_data=db_instance_data)
                    if rds_instance.raw_instance_data is not None:
                        result.append(rds_instance)

            ### end main processing ###
            if 'Marker' in response:
                if isinstance(response['Marker'], str):
                    if len(response['Marker']) > 0:
                        next_result = get_rds_instances(
                            aws_client=aws_client, 
                            next_token=response['Marker'], 
                            max_results_per_iteration=max_results_per_iteration, 
                            log_wrapper=log_wrapper
                        )
                        result = result + next_result
        except:
            log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    else:
        log_wrapper.warning(message='No RDS instances were fetched because the aws_client was not defined - failing gracefully...')
    return result


def get_service_client_default(service='ec2', region: str='us-east-1', target_profile: str=None, log_wrapper=LogWrapper()):
    client = None
    try:
        if service not in INSTANCE_CLASSES:
            raise Exception('Service "{}" not supported for this application yet'.format(service))
        if region not in get_regions_by_service(service=service, log_wrapper=log_wrapper):
            raise Exception('Service "{}" not available in selected region "{}"'.format(service, region))
        if target_profile is not None:
            session = boto3.Session(profile_name=target_profile)
            client = session.client(service, region_name=region)
        else:
            client = boto3.client(service, region_name=region)
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    if client is not None:
        log_wrapper.info(message='AWS Client connected to region "{}" for service "{}"'.format(region, service))
    else:
        log_wrapper.error(message='AWS Client could NOT connected to region "{}" for service "{}"'.format(region, service))
    return client


def collect_aws_instance_data(
    services: list=['ec2', 'rds'],
    all_regions: bool=True,
    regions: list=None,
    target_profile: str=None,
    log_wrapper=LogWrapper()
)->AWSInstanceCollection:
    instance_data_collection = AWSInstanceCollection(log_wrapper=log_wrapper)
    try:
        for service in services:
            if all_regions is True:
                regions = get_regions_by_service(service=service, log_wrapper=log_wrapper)
            for region in regions:
                client = get_service_client_default(service=service, region=region, target_profile=target_profile, log_wrapper=log_wrapper)
            instances = list()
            if service == 'ec2':
                instances = get_ec2_instances(
                    aws_client=client,
                    log_wrapper=log_wrapper
                )
            if service == 'rds':
                instances = get_rds_instances(
                    aws_client=client,
                    log_wrapper=log_wrapper
                )
            if len(instances) > 0:
                for instance in instances:
                    instance_data_collection.instances.append(instance)
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    return instance_data_collection

# EOF 
