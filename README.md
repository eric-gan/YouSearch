# YouSearch
Find what you want within YouTube videos

## Usage
Dependencies are currently supported on Python 3 and Python 2.7.X and can be found in `requirements.txt`.

To run the service, first run the following commands from Terminal
```
git clone https://github.com/eric-gan/YouSearch
cd YouSearch
python main.py
```

Next, in any browser, navigate to the localhost port the service is running on.

### PyTube 9.5.X
If the current version of PyTube you are using is `pytube 9.5.X`, some changes need to be made to be able to download the YouTube videos without running into translation errors with `urllib` <br>
Open Terminal and if PyTube is already installed, run
```
pip uninstall pytube
```
Otherwise, navigate to a temporary folder and run
```
git clone git://github.com/nficano/pytube.git
```
Next in any text editor, open `../pytube/pytube/mixins.py`. Starting from approximately line 42 to 66, replace the existing code block in the `apply_signature` method with the following code block instead.
```python
if ('signature=' in url or 
        ('s' not in stream and 
         ('&sig=' in url or '&lsig=' in url))):
    # For certain videos, YouTube will just provide them pre-signed, in
    # which case there's no real magic to download them and we can skip
    # the whole signature descrambling entirely.
    logger.debug('signature found, skip decipher')
    continue

if js is not None:
    signature = cipher.get_signature(js, stream['s'])
else:
    # signature not present in url (line 33), need js to descramble
    # TypeError caught in __main__
    raise TypeError('JS is None')

logger.debug(
    'finished descrambling signature for itag=%s\n%s',
    stream['itag'], pprint.pformat(
        {
            's': stream['s'],
            'signature': signature,
        }, indent=2,
    ),
)
stream_manifest[i]['url'] = url + '&sig=' + signature
``` 
After that, open `../pytube/pytube/cipher.py`. Starting from line 38, replace the existing pattern in the method `get_initial_function_name` with the following pattern.
```python
pattern = [
r'\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*encodeURIComponent\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'(?P<sig>[a-zA-Z0-9$]+)\s*=\s*function\(\s*a\s*\)\s*{\s*a\s*=\s*a\.split\(\s*""\s*\)',
r'(["\'])signature\1\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\.sig\|\|(?P<sig>[a-zA-Z0-9$]+)\(',
r'yt\.akamaized\.net/\)\s*\|\|\s*.*?\s*[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?:encodeURIComponent\s*\()?\s*(?P<si$',
r'\b[cs]\s*&&\s*[adf]\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\b[a-zA-Z0-9]+\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\bc\s*&&\s*a\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\(',
r'\bc\s*&&\s*[a-zA-Z0-9]+\.set\([^,]+\s*,\s*\([^)]*\)\s*\(\s*(?P<sig>[a-zA-Z0-9$]+)\('
]
``` 
Lastly in `../pytube/` directory, open Terminal and run
```
pip install .
```
The download process for YouTube videos should now be functional
## Debugging
The YouTube file in the S3 bucket is 0 KB or cannot download the video due to an error with `urllib`.
```
urllib2.HTTPError: HTTP Error 403: Forbidden
```
See section above regarding PyTube 9.5.X.
