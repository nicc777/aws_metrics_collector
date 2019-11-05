import os
from aws_metrics_collector import LogWrapper
from aws_metrics_collector.aws import collect_aws_instance_data
from aws_metrics_collector.utils import dict_to_json


database_file = '{}{}aws_instance_metric_statistics.sqlite'.format(os.getcwd(), os.sep)
dump_raw_json_to_file = True
json_file = '{}{}data.json'.format(os.getcwd(), os.sep)
services = ['ec2', 'rds']
all_regions = True
regions = None
target_profile = None
log_wrapper = LogWrapper()


def run():
    log_wrapper.info(message='START')
    log_wrapper.info(message='Database file to be used: {}'.format(database_file))
    data = collect_aws_instance_data(
        services=services,
        all_regions=all_regions,
        regions=regions,
        target_profile=target_profile,
        log_wrapper=log_wrapper
    )
    if dump_raw_json_to_file is True:
        if os.path.exists(json_file):
            log_wrapper.info(message='Removing exiting data file "{}"'.format(json_file))
            os.unlink(json_file)
        log_wrapper.info(message='Writing out raw data file to "{}"'.format(json_file))
        with open(json_file, 'w') as f:
            f.write(dict_to_json(data.to_dict()))
    log_wrapper.info(message='DONE')


if __name__ == '__main__':
    run()

# EOF
