import requests
from tqdm import tqdm
import os.path
import fnmatch
from functools import wraps
from hashlib import sha256
from io import open
import json
import logging
import os
import shutil
import tarfile
import tempfile
from urllib.parse import urlparse




def url_to_filename(url, etag=None):
    """
    Convert `url` into a hashed filename in a repeatable way.
    If `etag` is specified, append its hash to the URL's, delimited
    by a period.
    """
    url_bytes = url.encode('utf-8')
    url_hash = sha256(url_bytes)
    filename = url_hash.hexdigest()

    if etag:
        etag_bytes = etag.encode('utf-8')
        etag_hash = sha256(etag_bytes)
        filename += '.' + etag_hash.hexdigest()

    return filename


def http_get(url, temp_file):
    import requests
    from tqdm import tqdm
    req = requests.get(url, stream=True)
    content_length = req.headers.get('Content-Length')
    total = int(content_length) if content_length is not None else None
    progress = tqdm(unit="B", total=total)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()


def get_from_cache(url, cache_dir=None):
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code != 200:
            etag = None
        else:
            etag = response.headers.get("ETag")
    except EnvironmentError:
        etag = None

    filename = url_to_filename(url, etag)

    # get cache path to put the file
    cache_path = os.path.join(cache_dir, filename)

    # If we don't have a connection (etag is None) and can't identify the file
    # try to get the last downloaded one
    if not os.path.exists(cache_path) and etag is None:
        matching_files = fnmatch.filter(os.listdir(cache_dir), filename + '.*')
        matching_files = list(filter(lambda s: not s.endswith('.json'), matching_files))
        if matching_files:
            cache_path = os.path.join(cache_dir, matching_files[-1])

    if not os.path.exists(cache_path):
        # Download to temporary file, then copy to cache dir once finished.
        # Otherwise you get corrupt cache entries if the download gets interrupted.
        with tempfile.NamedTemporaryFile() as temp_file:
            # print("%s not found in cache, downloading to %s", url, temp_file.name)
            print('{} not found in cache, downloading to {}'.format(url, temp_file.name))

            http_get(url, temp_file)

            # we are copying the file before closing it, so flush to avoid truncation
            temp_file.flush()
            # shutil.copyfileobj() starts at the current position, so go to the start
            temp_file.seek(0)

            # print("copying %s to cache at %s", temp_file.name, cache_path)
            print('copying {} to cache at {}'.format(temp_file.name, cache_path))
            with open(cache_path, 'wb') as cache_file:
                shutil.copyfileobj(temp_file, cache_file)

            # print("creating metadata file for %s", cache_path)
            print('creating metadata file for {}'.format(cache_path))
            meta = {'url': url, 'etag': etag}
            meta_path = cache_path + '.json'
            with open(meta_path, 'w') as meta_file:
                output_string = json.dumps(meta)
                meta_file.write(output_string)

            # print("removing temp file %s", temp_file.name)
            print('removing temp file {}'.format(temp_file.name))

    return cache_path


def cached_path(url_or_filename, cache_dir=None):
    """
    Given something that might be a URL (or might be a local path),
    determine which. If it's a URL, download the file and cache it, and
    return the path to the cached file. If it's already a local path,
    make sure the file exists and then return the path.
    """
    
    parsed = urlparse(url_or_filename)

    if parsed.scheme in ('http', 'https', 's3'):
        # URL, so get it from the cache (downloading if necessary)
        return get_from_cache(url_or_filename, cache_dir)
    elif os.path.exists(url_or_filename):
        # File, and it exists.
        return url_or_filename
    elif parsed.scheme == '':
        # File, but it doesn't exist.
        raise EnvironmentError("file {} not found".format(url_or_filename))
    else:
        # Something unknown
        raise ValueError("unable to parse {} as a URL or as a local path".format(url_or_filename))


def load_model_file(archive_file, cache_dir):
    # redirect to the cache, if necessary
    try:
        resolved_archive_file = cached_path(archive_file, cache_dir)
    except EnvironmentError:
        print(
            "Archive name '{}' was not found in archive name list. "
            "We assumed '{}' was a path or URL but couldn't find any file "
            "associated to this path or URL.".format(
                archive_file,
                archive_file,
            )
        )
        return None

    if resolved_archive_file == archive_file:
        print("loading archive file {}".format(archive_file))
    else:
        print("loading archive file {} from cache at {}".format(
            archive_file, resolved_archive_file))

    # Extract archive to temp dir and replace .tar.bz2 if necessary
    tempdir = None
    if not os.path.isdir(resolved_archive_file):
        tempdir = tempfile.mkdtemp()
        print("extracting archive file {} to temp dir {}".format(
            resolved_archive_file, tempdir))
        ext = os.path.splitext(archive_file)[1][1:]
        with tarfile.open(resolved_archive_file, 'r:' + ext) as archive:
            top_dir = os.path.commonprefix(archive.getnames())
            archive.extractall(tempdir)
        os.remove(resolved_archive_file)
        shutil.move(os.path.join(tempdir, top_dir), resolved_archive_file)
        shutil.rmtree(tempdir)

    return resolved_archive_file

