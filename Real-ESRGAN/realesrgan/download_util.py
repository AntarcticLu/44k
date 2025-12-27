import os
import requests
from tqdm import tqdm


def load_file_from_url(url, model_dir=None, progress=True, file_name=None):
    """Load file from url.

    Args:
        url (str): URL to download file from.
        model_dir (str): The path to save the downloaded model. Default: None (current directory).
        progress (bool): Whether to show the download progress. Default: True.
        file_name (str): The downloaded file name. If None, use the file name in url. Default: None.

    Returns:
        str: Path to the downloaded file.
    """
    if model_dir is None:
        model_dir = os.getcwd()

    os.makedirs(model_dir, exist_ok=True)

    if file_name is None:
        file_name = os.path.basename(url)

    cached_file = os.path.join(model_dir, file_name)

    if os.path.exists(cached_file):
        return cached_file

    print(f'Downloading: "{url}" to {cached_file}')

    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(cached_file, 'wb') as f:
        if progress:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        else:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return cached_file
