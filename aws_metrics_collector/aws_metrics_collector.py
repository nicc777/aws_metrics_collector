import os
import argparse
import traceback
import sys
from aws_metrics_collector import LogWrapper
from aws_metrics_collector.aws import collect_aws_instance_data
from aws_metrics_collector.utils import dict_to_json


database_file = '{}{}aws_instance_metric_statistics.sqlite'.format(os.getcwd(), os.sep)
dump_raw_json_to_file = False
json_file = '{}{}data.json'.format(os.getcwd(), os.sep)
services = ['ec2', 'rds']
all_regions = True
regions = None
target_profile = None
log_wrapper = LogWrapper()
dummy_run = False


def parse_command_line_args(log_wrapper: LogWrapper=LogWrapper()):
    global json_file
    global dump_raw_json_to_file
    global dummy_run
    log_wrapper.info(message='Parsing command line arguments')
    args = None
    try:
        parser = argparse.ArgumentParser(
            prog='amcollect',
            description='Collect EC2 and/or RDS instance metric statics from all (or selected) regions in AWS'
        )
        parser.add_argument(
            '-f', '--json-file',
            nargs=1,
            action='store',
            help='When supplied, all collected data will be dumped to the supplied file as JSON data.'
        )
        parser.add_argument(
            '--dummy-run',
            action='store_true',
            help='When supplied, Don\'t perform and collections run (useful for testing command line parameter parsing during development)'
        )
        args = parser.parse_args()
        log_wrapper.info(message='Command line arguments: {}'.format(vars(args)))
        if args.json_file is not None:
            json_file = args.json_file
            dump_raw_json_to_file = True
    except:
        log_wrapper.error(message='EXCEPTION: {}'.format(traceback.format_exc()))
    log_wrapper.info(message='startup variable "database_file" : {}'.format(database_file))
    log_wrapper.info(message='startup variable "dump_raw_json_to_file" : {}'.format(dump_raw_json_to_file))
    log_wrapper.info(message='startup variable "json_file" : {}'.format(json_file))
    log_wrapper.info(message='startup variable "services" : {}'.format(services))
    log_wrapper.info(message='startup variable "all_regions" : {}'.format(all_regions))
    log_wrapper.info(message='startup variable "regions" : {}'.format(regions))
    log_wrapper.info(message='startup variable "target_profile" : {}'.format(target_profile))
    log_wrapper.info(message='startup variable "dummy_run" : {}'.format(dummy_run))
    if args is not None:
        if args.dummy_run is True:
            print('Dummy Run - please check the log file for details')
            sys.exit()


def run():
    parse_command_line_args()
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
