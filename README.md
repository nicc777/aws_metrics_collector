# AWS Metrics Collector

Collect AWS EC2 and RDS Instance Metrics for Local Analysis

The idea is to use the `boto3` library and using potentially multiple AWS accounts, collect metrics of all EC2 and RDS instances over a 24 hour period (customizable calender range).

The collected data will be stored in a local `sqlite` database. The data can then be analysed in any modern Spreadsheet application capable of connecting to the database.

## Installing from Source

Quick start, including the creation of a Python virtual environment (showing Linux based example):

```
$ cd ; mkdir git ; cd git
$ git clone https://github.com/nicc777/aws_metrics_collector.git
$ cd aws_metrics_collector
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip3 install boto3
(venv) $ python3 setup.py sdist
(venv) $ pip3 install dist/*
```
