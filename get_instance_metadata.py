"""
This script will fetch AWS EC2 instance metadata.
"""
import argparse
import json
import sys

import requests


def get_instance_metadata_token(
    ttl_seconds: int = 300,
    request_timeout: int = 10
) -> str:
    """Create a token for accessing the EC2 instance metadata service.

    Args:
        ttl_seconds (int): The time-to-live for the token in seconds.
            Default is 300 seconds (5 minutes).
        request_timeout (int): The timeout for the request in seconds.
            Default is 10 seconds.

    Returns:
        str: The instance metadata token.
    """
    url = "http://169.254.169.254/latest/api/token"
    headers = {"X-aws-ec2-metadata-token-ttl-seconds": str(ttl_seconds)}

    try:
        response = requests.put(
            url=url,
            headers=headers,
            timeout=request_timeout
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Could not fetch instance metadata token with error: {e}")
        sys.exit(1)


def fetch_instance_metadata_api(metadata_token: str, category: str = None) -> str:
    """Fetch the EC2 instance metadata API.

    Args:
        url (str): The URL to fetch metadata from.
        metadata_token (str): The instance metadata token.

    Returns:
        str: The instance metadata as a string.
    """
    url = "http://169.254.169.254/latest/meta-data"
    if category:
        url = f"{url}/{category}"

    headers = {"X-aws-ec2-metadata-token": metadata_token}

    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Could not fetch instance metadata with error: {e}")
        sys.exit(1)


def get_instance_metadata(
    metadata_token: str,
    category: str = None,
) -> dict[str, str | list[str] | dict[str, str]]:
    """Get the instance metadata.

    Args:
        metadata_token (str): The instance metadata token.
        category (str, optional): The specific metadata category to fetch.
            If not provided, all metadata will be fetched.

    Returns:
        dict[str, str | list[str] | dict[str, str]]: The instance metadata.
    """
    if not category:
        metadata_response = fetch_instance_metadata_api(
            metadata_token=metadata_token
        )
        return {"categories": metadata_response.splitlines()}

    metadata_response = fetch_instance_metadata_api(
        metadata_token=metadata_token,
        category=category
    )
    if "\n" in metadata_response:
        try:
            metadata_response = json.loads(metadata_response)
        except json.JSONDecodeError:
            return {category: metadata_response.splitlines()}
    return {category: metadata_response}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the AWS EC2 instance metadata."
    )
    parser.add_argument(
        "--category",
        type=str,
        help=(
            "The specific metadata category to fetch. If not provided, "
            "all metadata categories will be fetched."
        )
    )
    args = parser.parse_args()

    token = get_instance_metadata_token()
    result = get_instance_metadata(
        metadata_token=token,
        category=args.category
    )
    print(result)
