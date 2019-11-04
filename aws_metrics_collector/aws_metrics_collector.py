from aws_metrics_collector import LogWrapper
from aws_metrics_collector.aws import collect_aws_instance_data


def run():
    print('START')
    data = collect_aws_instance_data()


if __name__ == '__main__':
    run()

# EOF
