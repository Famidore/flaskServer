import json


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


if __name__ == "__main__":
    print(obtain_key("keys2.json", "twitter_api"))
