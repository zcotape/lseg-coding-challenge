# LSEG Coding Challenge

Query the metadata of an instance within AWS and provide a JSON formatted output.

## Pre-requisites

```text
$ pip install dependencies/requirements.txt
```

## Usage

```text
$ python get_instance_metadata.py --help
usage: get_instance_metadata.py [-h] [--category CATEGORY]

Fetch AWS EC2 instance metadata using the IMDSv2 API.

options:
  -h, --help           show this help message and exit
  --category CATEGORY  The specific metadata category to fetch. If not provided, all available metadata categories will be fetched.
```

Use `--category` argument to get any individual metadata key:

```text
$ python get_instance_metadata.py --category local-hostname
{'local-hostname': 'ip-10-100-100-100.ap-southeast-1.compute.internal'}

$ python get_instance_metadata.py --category network/interfaces/macs/12:34:56:78:90:ab/
{'network/interfaces/macs/12:34:56:78:90:ab/': ['device-number', 'interface-id', 'ipv4-associations/', 'local-hostname', 'local-ipv4s', 'mac', 'owner-id', 'public-hostname', 'public-ipv4s', 'security-group-ids', 'security-groups', 'subnet-id', 'subnet-ipv4-cidr-block', 'subnet-ipv6-cidr-blocks', 'vpc-id', 'vpc-ipv4-cidr-block', 'vpc-ipv4-cidr-blocks', 'vpc-ipv6-cidr-blocks']}

$ python get_instance_metadata.py --category network/interfaces/macs/12:34:56:78:90:ab/device-number
{'network/interfaces/macs/12:34:56:78:90:ab/device-number': '0'}
```

If `--category` is not provided, the script will show all available metadata categories:

```text
$ python get_instance_metadata.py
{'categories': ['ami-id', 'ami-launch-index', 'ami-manifest-path', 'block-device-mapping/', 'events/', 'hostname', 'identity-credentials/', 'instance-action', 'instance-id', 'instance-life-cycle', 'instance-type', 'local-hostname', 'local-ipv4', 'mac', 'metrics/', 'network/', 'placement/', 'profile', 'public-hostname', 'public-ipv4', 'public-keys/', 'reservation-id', 'security-groups', 'services/', 'system']}
```
