import json
from threading import Thread


def obtain_key(file_path: str = "keys.json", mode: str = "youtube_key"):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return str(data[mode])
    except FileNotFoundError:
        print("\nEnter your api key in the 'keys.json' file")
    except Exception as e:
        print(f"An error occurred when reading api key: {e}")
    return


class threadReturn(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None
    ):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


if __name__ == "__main__":
    print(obtain_key("keys2.json", "twitter_api"))
