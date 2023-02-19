import requests
import re


def main():
    def parse_page(url: str) -> tuple[None | str, int | None, int | None]:
        print(f"Going to parse: {url} ...")
        try:
            headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0",
            }
            print(f"Getting {url} ...")
            response = requests.get(url=url, headers=headers)
        except Exception as e:
            print("Get failed")
            return f"Get failed: {e}", None, None

        if not response:
            err = f"response is None"
            print(err)
            return err, None, None
        else:
            if response.status_code == 200:
                print("200 OK")
                print("Parsing ...")
                re_tag = re.compile("<\w.*>")
                re_tag_with_attr = re.compile("<\w*\s\w")
                tags_count = 0
                tags_with_attr_count = 0
                for tag in re_tag.findall(response.text):
                    tags_count += 1
                    if re_tag_with_attr.match(tag):
                        tags_with_attr_count += 1

                return None, tags_count, tags_with_attr_count
            else:
                return f"Status code: {response.status_code}", None, None

    url = "https://greenatom.ru"
    err, tags, tags_with_attr = parse_page(url=url)
    if err:
        print(f"Failed, error: {err}")
    print(f"Results: tags: {tags}, tags with attrs: {tags_with_attr}")


if __name__ == '__main__':
    main()
