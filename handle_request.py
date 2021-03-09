import requests
import argparse


def create_parser():
    """
    create the Command Line Interface
    :return: the arguments that the Command Line Interface has
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--JSON', type=str, help='the json file for PUT and POST requests')
    parser.add_argument('--GET', type=str, help='GET request; in the format of "GET url"')
    parser.add_argument('--POST', type=str, help='POST request; in the format of "POST {} url"')
    parser.add_argument('--PUT', type=str, help='PUT request; in the format of "PUT {} url"')
    parser.add_argument('--DELETE', type=str, help='DELETE request; in the format of "DELETE url"')
    return parser.parse_args()


if __name__ == '__main__':
    ARGS = create_parser()
    if ARGS.GET is not None:
        result = requests.get(ARGS.GET)
        print(result.text)
    if ARGS.PUT is not None:
        if ARGS.JSON is None:
            print("You must have a json object to do the PUT request!")
        else:
            requests.put(ARGS.PUT, json=ARGS.JSON)
    if ARGS.POST is not None:
        if ARGS.JSON is None:
            print("you must have something to POST!")
        else:
            requests.post(ARGS.POST, json=ARGS.JSON)
    if ARGS.DELETE is not None:
        requests.delete(ARGS.DELETE)
