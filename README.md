# LSEG Coding Challenge

Query the metadata of an instance within AWS and provide a JSON formatted output.

**Bonus Points**: The code allows for a particular data key to be retrieved individually

## Prerequisites

- Python 3.8 or greater
- [requests](https://github.com/psf/requests)

Or you can install dependencies with a provided requirements file:

```text
pip install dependencies/requirements.txt
```

## Usage

```text
$ python get_instance_metadata.py --help
usage: get_instance_metadata.py [-h] [--category CATEGORY]

Get the AWS EC2 instance metadata.

options:
  -h, --help           show this help message and exit
  --category CATEGORY  The specific metadata category to fetch. If not provided, all available metadata categories will be fetched.
```

Use `--category` argument to get any individual metadata key:

```text
$ python get_instance_metadata.py --category local-hostname
{
  "local-hostname": "ip-10-100-111-4.ap-southeast-1.compute.internal"
}

$ python get_instance_metadata.py --category placement/
{
  "availability-zone": "ap-southeast-1b",
  "availability-zone-id": "apse1-az2",
  "region": "ap-southeast-1"
}

$ python get_instance_metadata.py --category network/interfaces/macs/12:34:56:78:90:ab/
{
  "device-number": 0,
  "interface-id": "eni-03f7eff43183f902b",
  "ipv4-associations": {
    "REDACTED": "10.100.111.4"
  },
  "local-hostname": "ip-10-100-111-4.ap-southeast-1.compute.internal",
  "local-ipv4s": "10.100.111.4",
  "mac": "06:a1:e5:79:fa:e9",
  "owner-id": 153110037242,
  "public-hostname": "REDACTED",
  "public-ipv4s": "REDACTED",
  "security-group-ids": "sg-02af19f10f110cba7",
  "security-groups": "prod-infra-remote-access",
  "subnet-id": "subnet-0a40e86156852078e",
  "subnet-ipv4-cidr-block": "10.100.108.0/22",
  "subnet-ipv6-cidr-blocks": "2406:da18:86c:daf1:0:0:0:0/64",
  "vpc-id": "vpc-08b7188f5361f3942",
  "vpc-ipv4-cidr-block": "10.100.0.0/16",
  "vpc-ipv4-cidr-blocks": "10.100.0.0/16",
  "vpc-ipv6-cidr-blocks": "2406:da18:86c:da00:0:0:0:0/56"
}

$ python get_instance_metadata.py --category network/interfaces/macs/12:34:56:78:90:ab/device-number
{
  "network/interfaces/macs/12:34:56:78:90:ab/device-number": "0"
}
```

If `--category` is not provided, the script will show all EC2 instance metadata:

```text
$ python get_instance_metadata.py
{
  "ami-id": "ami-055ca4e1578cfe2f9",
  "ami-launch-index": 0,
  "ami-manifest-path": "(unknown)",
  "block-device-mapping": {
    "ami": "xvda",
    "root": "/dev/xvda"
  },
  "events": {
    "maintenance": {
      "history": [],
      "scheduled": []
    }
  },
  "hostname": "ip-10-100-111-4.ap-southeast-1.compute.internal",
  "identity-credentials": {
    "ec2": {
      "info": {
        "Code": "Success",
        "LastUpdated": "2025-06-27T04:07:10Z",
        "AccountId": "153110037242"
      },
      "security-credentials": {
        "ec2-instance": {
          "Code": "Success",
          "LastUpdated": "2025-06-27T04:07:08Z",
          "Type": "AWS-HMAC",
          "AccessKeyId": "REDACTED",
          "SecretAccessKey": "REDACTED",
          "Token": "REDACTED",
          "Expiration": "REDACTED"
        }
      }
    }
  },
  "instance-action": "none",
  "instance-id": "i-04c3cb2608f2404cd",
  "instance-life-cycle": "on-demand",
  "instance-type": "c6g.large",
  "local-hostname": "ip-10-100-111-4.ap-southeast-1.compute.internal",
  "local-ipv4": "10.100.111.4",
  "mac": "06:a1:e5:79:fa:e9",
  "metrics": {
    "vhostmd": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
  },
  "network": {
    "interfaces": {
      "macs": {
        "06:a1:e5:79:fa:e9": {
          "device-number": 0,
          "interface-id": "eni-03f7eff43183f902b",
          "ipv4-associations": {
            "REDACTED": "10.100.111.4"
          },
          "local-hostname": "ip-10-100-111-4.ap-southeast-1.compute.internal",
          "local-ipv4s": "10.100.111.4",
          "mac": "06:a1:e5:79:fa:e9",
          "owner-id": 153110037242,
          "public-hostname": "REDACTED",
          "public-ipv4s": "REDACTED",
          "security-group-ids": "sg-02af19f10f110cba7",
          "security-groups": "prod-infra-remote-access",
          "subnet-id": "subnet-0a40e86156852078e",
          "subnet-ipv4-cidr-block": "10.100.108.0/22",
          "subnet-ipv6-cidr-blocks": "2406:da18:86c:daf1:0:0:0:0/64",
          "vpc-id": "vpc-08b7188f5361f3942",
          "vpc-ipv4-cidr-block": "10.100.0.0/16",
          "vpc-ipv4-cidr-blocks": "10.100.0.0/16",
          "vpc-ipv6-cidr-blocks": "2406:da18:86c:da00:0:0:0:0/56"
        }
      }
    }
  },
  "placement": {
    "availability-zone": "ap-southeast-1b",
    "availability-zone-id": "apse1-az2",
    "region": "ap-southeast-1"
  },
  "profile": "default-hvm",
  "public-hostname": "REDACTED",
  "public-ipv4": "REDACTED",
  "public-keys": {
    "0": "REDACTED"
  },
  "reservation-id": "r-0a77d92a8e9591958",
  "security-groups": "prod-infra-remote-access",
  "services": {
    "domain": "amazonaws.com",
    "partition": "aws"
  },
  "system": "nitro"
}
```
