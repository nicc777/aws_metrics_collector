from setuptools import setup, find_packages
from os import path
from io import open
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='aws_metrics_collector',
    version='0.0.1',
    download_url = 'https://github.com/nicc777/aws_metrics_collector/releases/download/release-0.0.1/aws_metrics_collector-0.0.1.tar.gz',
    description='Collect AWS EC2 and RDS Instance Metrics for Local Analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nicc777/aws_metrics_collector',
    author='Nico Coetzee',
    author_email='nicc777@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='aws ec2 rds metrics data sqlite',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6.*, <4',
    install_requires=['boto3'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    entry_points={
        'console_scripts': [
            'amcollect=aws_metrics_collector.aws_metrics_collector:run',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/nicc777/aws_metrics_collector/issues',
        'Source': 'https://github.com/nicc777/aws_metrics_collector',
    },
)
