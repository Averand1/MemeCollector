import os as _os
import dotenv as _dotenv
import praw as _praw
import urllib.parse as parse
import requests as _requests
import shutil as _shutil

_dotenv.load_dotenv()  # Loads our env file

# Creating Reddit Client


def _create_reddit_client():
    client = _praw.Reddit(
        # Using the info stored in .env file, make sure your id/keys are private
        client_id=_os.environ["CLIENT_ID"],
        client_secret=_os.environ["CLIENT_SECRET"],
        user_agent=_os.environ["USER_AGENT"]
    )
    return client


def _is_image(post):  # Checks if you can post image or not in a subreddit
    try:
        return post.post_hint == "image"
    except AttributeError:
        return False

# Gets URLs from given subreddits


def _get_image_urls(client: _praw.Reddit, subreddit_name: str, limit: int):
    # We don't want random memes, we want the user voted one, limit is for how many urls we want
    hot_memes = client.subreddit(subreddit_name).hot(limit=limit)
    # Make those urls into a list
    image_urls = list()
    for post in hot_memes:
        # Many subreddits have posts with no image, this checks the ones with image and returns image url
        if _is_image(post):
            image_urls.append(post.url)

    return image_urls  # returing image url

# Getting image name


def _get_image_name(image_url: str) -> str:
    image_name = parse.urlparse(image_url)
    return _os.path.basename(image_name.path)


def _create_folder(folder_name: str):
    """
    If the folder doesn't exist, create the folder using the given name
    """

    try:
        _os.mkdir(folder_name)
    except OSError:
        print("Something happened")
    else:
        print("folder created")


def _download_image(folder_name: str, raw_response, image_name: str):
    _create_folder(folder_name)
    with open(f"{folder_name}/{image_name}", "wb") as image_file:
        _shutil.copyfileobj(raw_response, image_file)


def _collect_memes(subreddit_name: str, limit: int = 20):
    """
    Collects the images from the urls and stores them into 
    the folders name after subreddits
    """
    client = _create_reddit_client()
    image_urls = _get_image_urls(
        client=client, subreddit_name=subreddit_name, limit=limit)
    for image_url in image_urls:
        image_name = _get_image_name(image_url)
        response = _requests.get(image_url, stream=True)

        # Need this to be true to get images
        if response.status_code == 200:
            response.raw.decode_content = True
            _download_image(subreddit_name, response.raw, image_name)


if __name__ == "__main__":
    _collect_memes("ProgrammerHumor")
