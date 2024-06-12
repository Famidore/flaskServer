import json
from threading import Thread


def obtain_key(
    file_path: str = "CONFIG.json",
    mode: str = "youtube_key",
    reneder_whole: bool = False,
):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            if not reneder_whole:
                return str(data[mode])
            else:
                return [list(data.keys()), list(data.values())]
    except FileNotFoundError:
        print("\nEnter your api key in the 'CONFIG.json' file!")
    except Exception as e:
        print(f"An error occurred when reading api key: {e}!")
    return


def update_config(file_path: str = "CONFIG.json", data: list = None):
    if data:
        try:
            with open(file_path, "r") as reading:
                content = json.load(reading)
                keys = list(content.keys())
            reading.close()
            with open(file_path, "w") as writing:
                new_content = {}
                for key, value in zip(keys, data):
                    new_content[key] = value
                json.dump(new_content, writing)
                return
        except FileNotFoundError:
            print("\nThe CONFIG.json file is missing!")
        except Exception as e:
            print(f"An error occurred when reading api key: {e}!")
        return
    else:
        print("New data cannot be empty!")


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


def translate_media_name(input):
    """
    1 -> filmweb
    2 -> reddit
    3 -> wykop
    4 -> youutube
    """
    if input == 1:
        return "filmweb"
    elif input == 2:
        return "reddit"
    elif input == 3:
        return "wykop"
    elif input == 4:
        return "youtube"
    else:
        raise TypeError("Error during translation of media name")


if __name__ == "__main__":
    # print(obtain_key(reneder_whole=True))
    update_config(data=["test", "groszek", "tesss"])
