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


def fetch_instance_metadata_api(
    metadata_token: str,
    category: str = "",
    request_timeout: int = 10
) -> str:
    """Fetch the EC2 instance metadata API.

    Args:
        metadata_token (str): The instance metadata token.
        category (str, optional): The specific metadata category to fetch.
            If not provided, all metadata will be fetched.
        request_timeout (int): The timeout for the request in seconds.
            Default is 10 seconds.

    Returns:
        str: The instance metadata as a string.
    """
    url = "http://169.254.169.254/latest/meta-data/"
    if category:
        url = url + category

    headers = {"X-aws-ec2-metadata-token": metadata_token}

    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=request_timeout
        )
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Could not fetch instance metadata with error: {e}")
        sys.exit(1)


def get_instance_metadata(
    metadata_token: str,
    category: str = "",
) -> dict[str, str | list[str] | dict[str, str]]:
    """Get the instance metadata.

    Args:
        metadata_token (str): The instance metadata token.
        category (str, optional): The specific metadata category to fetch.
            If not provided, all metadata will be fetched.

    Returns:
        dict[str, str | list[str] | dict[str, str]]: The instance metadata.
    """
    metadata_response = fetch_instance_metadata_api(
        metadata_token=metadata_token,
        category=category
    )

    categories = metadata_response.split("\n")
    is_category_path = (
        metadata_response.endswith("/") or category.endswith("/")
    )

    if len(categories) > 1 or is_category_path:
        metadata = {}
        if category and not category.endswith("/"):
            prefix = f"{category}/"
        else:
            prefix = category

        for item in categories:
            sub_category = f"{prefix}{item}"
            if item.endswith("/"):
                metadata[item.rstrip("/")] = get_instance_metadata(
                    metadata_token=metadata_token,
                    category=sub_category
                )
            else:
                if sub_category.startswith("public-keys/"):
                    public_key_id = item.split("=")[0]
                    metadata[public_key_id] = fetch_instance_metadata_api(
                        metadata_token=metadata_token,
                        category=f"public-keys/{public_key_id}/openssh-key"
                    )
                else:
                    metadata_value = fetch_instance_metadata_api(
                        metadata_token=metadata_token,
                        category=sub_category
                    )
                    try:
                        metadata[item] = json.loads(metadata_value)
                    except json.JSONDecodeError:
                        metadata[item] = metadata_value
        return metadata
    return {category: metadata_response}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get the AWS EC2 instance metadata."
    )
    parser.add_argument(
        "--category",
        type=str,
        default="",
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
    print(json.dumps(result, indent=2))
