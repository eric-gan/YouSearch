# YouSearch
Find what you want within YouTube videos

## Usage
Dependencies are currently supported on Python 3 and Python 2.7.X and can be found in `requirements.txt`.

### PyTube 9.5.X
If the current version of PyTube you are using is `pytube 9.5.X`, some changes need to be made to be able to download the YouTube videos without running into errors with `urllib` <br>
Open Terminal and if PyTube is already installed, run
```
pip uninstall pytube
```
Otherwise, navigate to a temporary folder and run
```
git clone git://github.com/nficano/pytube.git
```
Next in any text editor, open `pytube/pytube/mixins.py`. Starting from approximately line 42 to 66, replace the existing similar code with the following code block instead
```
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

## Debugging
Cannot download the video due to an error with `urllib`.
```
urllib2.HTTPError: HTTP Error 403: Forbidden
```
See section above regarding PyTube 9.5.X
