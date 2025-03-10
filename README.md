**This fork adds additional tags for Zotify which may or may not be compliant
with relevant standards.**

**It is highly recommended you use one of the upstream versions for use outside
of Zotify. No support will be given for other use cases.**

# music-tag

music-tag is a library for editing audio metadata with an interface
that does not depend on the underlying file format. In other words, editing
mp3 files shouldn not be any different than flac, m4a, ... This library is
just a layer on top of [mutagen](https://mutagen.readthedocs.io/en/latest/),
which does all the heavy lifting.

## Formats

The following file formats are actively tested.

- ``aac``
- ``aiff``
- ``dsf``
- ``flac``
- ``m4a``
- ``mp3``
- ``ogg``
- ``opus``
- ``wav``
- ``wv``

## Keys

Metadata is available using a dictionary-like interface with the following keys.
Keys are not case sensitive and can contain arbitrary whitespace, '-', and '_'
characters. In other words, ``Album Artist``, ``album-artist``, and
``album_artist`` are all synonyms for ``albumartist``. Also, ``disk`` is synonymous with ``disc``.

- ``album``
- ``albumartist``
- ``artist``
- ``artwork``
- ``comment``
- ``compilation``
- ``composer``
- ``discnumber``
- ``genre``
- ``label``
- ``lyrics``
- ``totaldiscs``
- ``totaltracks``
- ``tracknumber``
- ``tracktitle``
- ``year``
- ``isrc``
- ``albumartistsort``
- ``albumsort``
- ``artistsort``
- ``composersort``
- ``titlesort``
- ``work``
- ``movement``
- ``movementtotal``
- ``movementnumber``
- ``key``
- ``media``
- ``musicbrainzartistid``
- ``musicbrainzdiscid``
- ``musicbrainzoriginalartistid``
- ``musicbrainzoriginalalbumid``
- ``musicbrainzrecordingid``
- ``musicbrainzalbumartistid``
- ``musicbrainzreleasegroupid``
- ``musicbrainzalbumid``
- ``musicbrainztrackid``
- ``musicbrainzworkid``
- ``musicipfingerprint``
- ``musicippuid``
- ``acoustidid``
- ``acoustidfingerprint``
- ``subtitle``
- ``discsubtitle``
- ``#bitrate`` (read only)
- ``#codec`` (read only)
- ``#length`` (read only)
- ``#channels`` (read only)
- ``#bitspersample`` (read only)
- ``#samplerate`` (read only)

## Examples

### Reading tags

``` python
import music_tag

f = music_tag.load_file("music-tag/sample/440Hz.m4a")

# dict access returns a MetadataItem
title_item = f['title']

# MetadataItems keep track of multi-valued keys
title_item.values  # -> ['440Hz']

# A single value can be extracted
title_item.first  # -> '440Hz'
title_item.value  # -> '440Hz'

# MetadataItems can also be cast to a string
str(title_item)  # -> '440Hz'
```

### Setting tags

``` python
# tags can be set as if the file were a dictionary
f['title'] = '440Hz'

# additional values can be appended to the tags
f.append_tag('title', 'subtitle')
title_item.values  # -> ['440Hz', 'subtitle']
title_item.first  # -> '440Hz'
title_item.value  # -> '440Hz, subtitle'
str(title_item)  # -> '440Hz, subtitle'
```

### Removing tags

``` python
del f['title']
f.remove_tag('title')
```

### Album artwork

Album artwork is wrapped in an object that keeps track of some of the
extra metadata associated with images. Note that some album art functionality
requires the Pillow (modern day PIL) library.

``` python
# get artwork
art = f['artwork']

# Note: `art` is a MetadataItem. Use ``art.value`` if there is
#       only one image embeded in the file. This will raise a
#       ValueError if there is more than one image. You can also
#       use ``art.first``, or iterate through ``art.values``.

art.first.mime  # -> 'image/jpeg'
art.first.width  # -> 1280
art.first.height  # -> 1280
art.first.depth  # -> 24
art.first.data  # -> b'... raw image data ...'

# set artwork
with open('music_tag/test/sample/imgA.jpg', 'rb') as img_in:
    f['artwork'] = img_in.read()
with open('music_tag/test/sample/imgB.jpg', 'rb') as img_in:
    f.append_tag('artwork', img_in.read())

# Make a thumbnail (requires Pillow)
art.first.thumbnail([64, 64])  # -> pillow image
art.first.raw_thumbnail([64, 64])  # -> b'... raw thumbnail data ...'
```

### Saving tags

``` python
# finally, you can bounce the edits to disk
f.save()
```

### Skipping Type Normalization

By default, tags are validated and normalized. For instance, track numbers
and years are return as integers. Some tag formats store everything as strings
to enable things like leading zeros in tracknumbers (i.e., track '01'). I think
this is ugly, but you can use the file object's ``raw`` property if you like
this kind of thing.

``` python
f.raw['tracknumber'] = '01'
f.raw['tracknumber'].value  # -> '01'
```

## Resolvers

Some tags may not exist in a file, but there could be enough information to
discern the correct value. For instance, the ``album artist`` tag is probably
equal to the ``artist`` tag, or ``"Various Artists"`` if the ``compilation``
flag is set. Here are some examples,

``` python
f['album artist'] = 'Brian'
f.resolve('album artist')  # <- 'Brian'
f['artist'] = 'Brian'
del f['album artist']
f['compilation'] = False
f.resolve('album artist')  # <- 'Brian'
f['compilation'] = True
f.resolve('album artist')  # <- 'Various Artists'

del f['compilation']
f['album artist'] = 'Various Artists'
f.resolve('compilation')  # <- True
f['album artist'] = 'Brian'
f.resolve('compilation')  # <- False
```

## Command Line Tool

The music_tag package can be used as a CLI to get / set tags. Here are some
examples,

### Printing Tags

``` bash
# Print tags from all audio files in sample directory
python -m music_tag --print ./sample

# Print specific tags from all audio files in sample directory      
python -m music_tag --print --tags="Title : Album" ./sample

# Write tags from all audio files in sample directory to a csv file
python -m music_tag --to-csv tags.csv ./sample

# Write specific tags from all audio files in sample directory to a csv file
python -m music_tag --tags="Title : Album" --to-csv tags.csv ./sample
```

### Setting Tags
``` bash
# Set a couple tags for multiple files      
python -m music_tag --set "genre:Pop" --set "comment:cli test" \
    ./sample/440Hz.aac ./sample/440Hz.flac

# Write tags from csv file to audio files (assuming file paths in
# the csv file are relative to the sample directory
python -m music_tag --from-csv tags.csv
```
