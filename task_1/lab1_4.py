import requests
import re


def main():
    def get_ip() -> None | str:
        url = "https://ifconfig.me"
        headers = {
            "user-agent": "curl",
        }
        try:
            response = requests.get(url=url, headers=headers)
        except:
            return None
        if response and (response.status_code == 200):
            return response.text
        return None

    result = get_ip()
    if not result:
        print(f"Failed to get my ip")
    print(f"Result: {result}")


if __name__ == '__main__':
    main()
