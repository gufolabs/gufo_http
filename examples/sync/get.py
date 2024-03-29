import sys

from gufo.http.sync_client import HttpClient


def main(url: str) -> None:
    with HttpClient() as client:
        r = client.get(url)
        if r.status != 200:
            print(f"Invalid response code: {r.status}")
            return
        print(r.content.decode())


main(sys.argv[1])
