#!/usr/bin/env python
# coding: utf-8

# FIXME: there's probably a more standard way of setting desc or repeated tags
# FIXME: there's probably a better way of dealing with pic_type

import mutagen
import mutagen.id3
import mutagen.easyid3
import mutagen.mp3
import mutagen.trueaudio

from music_tag import util
from music_tag.file import Artwork, AudioFile, MetadataItem, TAG_MAP_ENTRY


def get_tracknumA(afile, norm_key):
    return util.get_easy_tracknum(afile, norm_key, _tag_name='TRK')
def set_tracknumA(afile, norm_key, val):
    return util.set_easy_tracknum(afile, norm_key, val, _tag_name='TRK')
def rm_tracknumA(afile, norm_key):
    return util.rm_easy_tracknum(afile, norm_key, _tag_name='TRK')
def get_totaltracksA(afile, norm_key):
    return util.get_easy_totaltracks(afile, norm_key, _tag_name='TRK')
def set_totaltracksA(afile, norm_key, val):
    return util.set_easy_totaltracks(afile, norm_key, val, _tag_name='TRK')
def rm_totaltracksA(afile, norm_key):
    return util.rm_easy_totaltracks(afile, norm_key, _tag_name='TRK')

def get_discnumA(afile, norm_key):
    return util.get_easy_discnum(afile, norm_key, _tag_name='TPA')
def set_discnumA(afile, norm_key, val):
    return util.set_easy_discnum(afile, norm_key, val, _tag_name='TPA')
def rm_discnumA(afile, norm_key):
    return util.rm_easy_discnum(afile, norm_key, _tag_name='TPA')
def get_totaldiscsA(afile, norm_key):
    return util.get_easy_totaldiscs(afile, norm_key, _tag_name='TPA')
def set_totaldiscsA(afile, norm_key, val):
    return util.set_easy_totaldiscs(afile, norm_key, val, _tag_name='TPA')
def rm_totaldiscsA(afile, norm_key):
    return util.rm_easy_totaldiscs(afile, norm_key, _tag_name='TPA')

def get_tracknumB(afile, norm_key):
    return util.get_easy_tracknum(afile, norm_key, _tag_name='TRCK')
def set_tracknumB(afile, norm_key, val):
    return util.set_easy_tracknum(afile, norm_key, val, _tag_name='TRCK')
def rm_tracknumB(afile, norm_key):
    return util.rm_easy_tracknum(afile, norm_key, _tag_name='TRCK')
def get_totaltracksB(afile, norm_key):
    return util.get_easy_totaltracks(afile, norm_key, _tag_name='TRCK')
def set_totaltracksB(afile, norm_key, val):
    return util.set_easy_totaltracks(afile, norm_key, val, _tag_name='TRCK')
def rm_totaltracksB(afile, norm_key):
    return util.rm_easy_totaltracks(afile, norm_key, _tag_name='TRCK')

def get_discnumB(afile, norm_key):
    return util.get_easy_discnum(afile, norm_key, _tag_name='TPOS')
def set_discnumB(afile, norm_key, val):
    return util.set_easy_discnum(afile, norm_key, val, _tag_name='TPOS')
def rm_discnumB(afile, norm_key):
    return util.rm_easy_discnum(afile, norm_key, _tag_name='TPOS')
def get_totaldiscsB(afile, norm_key):
    return util.get_easy_totaldiscs(afile, norm_key, _tag_name='TPOS')
def set_totaldiscsB(afile, norm_key, val):
    return util.set_easy_totaldiscs(afile, norm_key, val, _tag_name='TPOS')
def rm_totaldiscsB(afile, norm_key):
    return util.rm_easy_totaldiscs(afile, norm_key, _tag_name='TPOS')

def get_pictures(afile, norm_key):
    pics = afile.mfile.tags.getall('APIC') + afile.mfile.tags.getall('PIC')
    artworks = []
    for p in pics:
        artworks.append(Artwork(p.data, pic_type=p.type))
    return MetadataItem(Artwork, None, artworks)

def set_pictures(afile, norm_key, artworks):
    if afile.mfile.tags.getall('APIC'):
        kls = mutagen.id3.APIC
    elif afile.mfile.tags.getall('PIC'):
        kls = mutagen.id3.PIC
    else:
        if afile.mfile.tags.version[:2] == (2, 2):
            kls = mutagen.id3.PIC
        else:
            kls = mutagen.id3.APIC

    tag = str(kls.__name__).strip(':')
    afile.mfile.tags.delall(tag)
    for i, art in enumerate(artworks.values):
        if kls == mutagen.id3.PIC:
            mime = {
                'image/jpeg': 'JPG',
                'image/jpg': 'JPG',
                'image/png': 'PNG'
            }[art.mime.lower()]
        else:
            mime = art.mime
        afile.mfile.tags.add(kls(data=art.raw, type=art.pic_type, desc=str(i),
                                 mime=mime))

def rm_pictures(afile, norm_key):
    afile.mfile.tags.delall('APIC')
    afile.mfile.tags.delall('PIC')

# https://github.com/tilo/ID3/tree/master/docs

_TAG_MAP_ID3_1 = {
    'title': TAG_MAP_ENTRY(getter='title', setter='title', type=str),
    'artist': TAG_MAP_ENTRY(getter='artist', setter='artist', type=str),
    'album': TAG_MAP_ENTRY(getter='album', setter='album', type=str),
    'year': TAG_MAP_ENTRY(getter='year', setter='year', type=int,
                          sanitizer=util.sanitize_year),
    'comment': TAG_MAP_ENTRY(getter='comment', setter='comment', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter='track', setter='track', type=int, sanitizer=util.sanitize_int),
    'genre': TAG_MAP_ENTRY(getter='genre', setter='genre', type=str),
}

_TAG_MAP_ID3_2_2 = {
    'title': TAG_MAP_ENTRY(getter='TT2', setter='TT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TP1', setter='TP1', type=str),
    'album': TAG_MAP_ENTRY(getter='TAL', setter='TAL', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TP2', setter='TP2', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCM', setter='TCM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumA,
                                 setter=set_tracknumA,
                                 remover=rm_tracknumA,
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksA,
                                 setter=set_totaltracksA,
                                 remover=rm_totaltracksA,
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumA,
                                setter=set_discnumA,
                                remover=rm_discnumA,
                                type=int,
                                sanitizer=util.sanitize_int),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsA,
                                setter=set_totaldiscsA,
                                remover=rm_totaldiscsA,
                                type=int,
                                sanitizer=util.sanitize_int),
    'genre': TAG_MAP_ENTRY(getter='TCO', setter='TCO', type=str),
    'year': TAG_MAP_ENTRY(getter=('TYE', 'TDA', 'TRD', 'TOR'),
                          setter=('TYE', 'TDA', 'TRD', 'TOR'),
                          type=int,
                          sanitizer=util.sanitize_year),
    'isrc': TAG_MAP_ENTRY(getter='TRC', setter='TRC', type=str),
    # 'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str,
    #                          sanitizer=util.sanitize_bool),
    # 'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    # 'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=int),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             remover=rm_pictures,
                             type=Artwork),
}

_TAG_MAP_ID3_2_3 = {
    'title': TAG_MAP_ENTRY(getter='TIT2', setter='TIT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TPE1', setter='TPE1', type=str),
    'album': TAG_MAP_ENTRY(getter='TALB', setter='TALB', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TPE2', setter='TPE2', type=str),
    'conductor': TAG_MAP_ENTRY(getter='TPE3', setter='TPE3', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCOM', setter='TCOM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumB,
                                 setter=set_tracknumB,
                                 remover=rm_tracknumB,
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksB,
                                 setter=set_totaltracksB,
                                 remover=rm_totaltracksB,
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumB,
                                setter=set_discnumB,
                                remover=rm_discnumB,
                                type=int,
                                sanitizer=util.sanitize_int),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsB,
                                setter=set_totaldiscsB,
                                remover=rm_totaldiscsB,
                                type=int,
                                sanitizer=util.sanitize_int),
    'genre': TAG_MAP_ENTRY(getter='TCON', setter='TCON', type=str),
    'year': TAG_MAP_ENTRY(getter=('TORY', 'TYER', 'TDAT', 'TDRC'),
                          setter=('TORY', 'TYER', 'TDAT', 'TDRC'),
                          type=int, sanitizer=util.sanitize_year),
    'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str),
    'label': TAG_MAP_ENTRY(getter='TPUB', setter='TPUB', type=str),
    'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    'isrc': TAG_MAP_ENTRY(getter='TSRC', setter='TSRC', type=str),
    'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=int,
                                 sanitizer=util.sanitize_bool),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             remover=rm_pictures,
                             type=Artwork),
}

_TAG_MAP_ID3_2_4 = {
    'title': TAG_MAP_ENTRY(getter='TIT2', setter='TIT2', type=str),
    'artist': TAG_MAP_ENTRY(getter='TPE1', setter='TPE1', type=str),
    'album': TAG_MAP_ENTRY(getter='TALB', setter='TALB', type=str),
    'albumartist': TAG_MAP_ENTRY(getter='TPE2', setter='TPE2', type=str),
    'conductor': TAG_MAP_ENTRY(getter='TPE3', setter='TPE3', type=str),
    'composer': TAG_MAP_ENTRY(getter='TCOM', setter='TCOM', type=str),
    'tracknumber': TAG_MAP_ENTRY(getter=get_tracknumB,
                                 setter=set_tracknumB,
                                 remover=('TRK', 'TRCK'),
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'totaltracks': TAG_MAP_ENTRY(getter=get_totaltracksB,
                                 setter=set_totaltracksB,
                                 remover=('TRK', 'TRCK'),
                                 type=int,
                                 sanitizer=util.sanitize_int),
    'discnumber': TAG_MAP_ENTRY(getter=get_discnumB,
                                setter=set_discnumB,
                                remover=('TPA', 'TPOS'),
                                type=int,
                                sanitizer=util.sanitize_int),
    'totaldiscs': TAG_MAP_ENTRY(getter=get_totaldiscsB,
                                setter=set_totaldiscsB,
                                remover=('TPA', 'TPOS'),
                                type=int,
                                sanitizer=util.sanitize_int),
    'genre': TAG_MAP_ENTRY(getter='TCON', setter='TCON',
                           type=str),
    'year': TAG_MAP_ENTRY(getter=('TDOR', 'TORY', 'TYER', 'TDAT', 'TDRC'),
                          setter=('TDOR', 'TYER', 'TDAT', 'TDRC'),
                          type=int,
                          sanitizer=util.sanitize_year),
    'comment': TAG_MAP_ENTRY(getter='COMM', setter='COMM', type=str),
    'label': TAG_MAP_ENTRY(getter='TPUB', setter='TPUB', type=str),
    'lyrics': TAG_MAP_ENTRY(getter='USLT', setter='USLT', type=str),
    'isrc': TAG_MAP_ENTRY(getter='TSRC', setter='TSRC', type=str),
    'compilation': TAG_MAP_ENTRY(getter='TCMP', setter='TCMP', type=int, sanitizer=util.sanitize_bool),

    'artwork': TAG_MAP_ENTRY(getter=get_pictures, setter=set_pictures,
                             remover=rm_pictures,
                             type=Artwork),

    'albumartistsort': TAG_MAP_ENTRY(getter='TSO2', setter='TSO2', type=str),
    'albumsort': TAG_MAP_ENTRY(getter='TSOA', setter='TSOA', type=str),
    'artistsort': TAG_MAP_ENTRY(getter='TSOP', setter='TSOP', type=str),
    'composersort': TAG_MAP_ENTRY(getter='TSOC', setter='TSOC', type=str),
    'titlesort': TAG_MAP_ENTRY(getter='TSOT', setter='TSOT', type=str),
    'work': TAG_MAP_ENTRY(getter=('TIT1', 'TXXX:WORK'), setter=('TIT1', 'TXXX:WORK'), type=str),
    'movementname': TAG_MAP_ENTRY(getter='MVNM', setter='MVNM', type=str),
    'movementtotal': TAG_MAP_ENTRY(getter='MVIN', setter='MVIN', type=int, sanitizer=util.sanitize_int),
    'movement': TAG_MAP_ENTRY(getter='MVIN', setter='MVIN', type=int, sanitizer=util.sanitize_int),
    'key': TAG_MAP_ENTRY(getter='TKEY', setter='TKEY', type=str),
    'media': TAG_MAP_ENTRY(getter='TMED', setter='TMED', type=str),
    'showmovement': TAG_MAP_ENTRY(getter='TXXX:SHOWMOVEMENT', setter='TXXX:SHOWMOVEMENT', type=int, sanitizer=util.sanitize_bool),

    'musicbrainzartistid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Artist Id', setter='TXXX:MusicBrainz Artist Id', type=str),
    'musicbrainzdiscid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Disc Id', setter='TXXX:MusicBrainz Disc Id', type=str),
    'musicbrainzoriginalartistid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Original Artist Id', setter='TXXX:MusicBrainz Original Artist Id', type=str),
    'musicbrainzoriginalalbumid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Original Album Id', setter='TXXX:MusicBrainz Original Album Id', type=str),
    'musicbrainzrecordingid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Track Id', setter='TXXX:MusicBrainz Track ID', type=str),
    'musicbrainzalbumartistid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Album Artist Id', setter='TXXX:MusicBrainz Album Artist Id', type=str),
    'musicbrainzreleasegroupid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Release Group Id', setter='TXXX:MusicBrainz Release Group Id', type=str),
    'musicbrainzalbumid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Album Id', setter='TXXX:MusicBrainz Album Id', type=str),
    'musicbrainztrackid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Release Track Id', setter='TXXX:MusicBrainz Release Track Id', type=str),
    'musicbrainzworkid': TAG_MAP_ENTRY(getter='TXXX:MusicBrainz Work Id', setter='TXXX:MusicBrainz Work Id', type=str),

    'musicipfingerprint': TAG_MAP_ENTRY(getter='TXXX:MusicMagic Fingerprint', setter='TXXX:MusicMagic Fingerprint', type=str),
    'musicippuid': TAG_MAP_ENTRY(getter='TXXX:MusicIP PUID', setter='TXXX:MusicIP PUID', type=str),
    'acoustidid': TAG_MAP_ENTRY(getter='TXXX:Acoustid Id', setter='TXXX:Acoustid Id', type=str),
    'acoustidfingerprint': TAG_MAP_ENTRY(getter='TXXX:Acoustid Fingerprint', setter='TXXX:Acoustid Fingerprint', type=str),

    'subtitle': TAG_MAP_ENTRY(getter='TIT3', setter='TIT3', type=str),
    'discsubtitle': TAG_MAP_ENTRY(getter='TSST', setter='TSST', type=str),
}


class Id3File(AudioFile):
    tag_format = "Id3"
    mutagen_kls = mutagen.id3.ID3FileType

    def __init__(self, filename, **kwargs):
        mfile = kwargs.get('_mfile', None)
        if mfile is None:
            mfile = mutagen.File(filename)
            kwargs['_mfile'] = mfile

        if mfile.tags:
            id3_ver = mfile.tags.version[:2]
        else:
            id3_ver = (2, 4)

        # by default, mutagen presents all files using id3v2.4
        if id3_ver[0] == 1:
            self._TAG_MAP = _TAG_MAP_ID3_2_4
        elif id3_ver == (2, 2):
            self._TAG_MAP = _TAG_MAP_ID3_2_4
        elif id3_ver == (2, 3):
            self._TAG_MAP = _TAG_MAP_ID3_2_4
        elif id3_ver == (2, 4):
            self._TAG_MAP = _TAG_MAP_ID3_2_4
        else:
            raise NotImplementedError("Unexpected id3 tag version: {0}"
                                      "".format(mfile.tags.version))

        super(Id3File, self).__init__(filename, **kwargs)

    def _ft_getter(self, key):
        vals = self.mfile.tags.getall(key)
        ret = []
        for val in vals:
            if isinstance(val.text, (list, tuple)):
                ret += [str(t) for t in val.text]
            else:
                ret += [str(val.text)]
        if not ret:
            ret = None
        return ret

    def _ft_setter(self, key, md_val, appendable=True):
        self.mfile.tags.delall(key)
        kls = getattr(mutagen.id3, key.split(':')[0])

        kwargs = {}
        _o = kls()
        if hasattr(_o, 'lang'):
            # so, it's a little anglo-centric to do this, but
            # this matches the behavior of kid3 and MusicBrainz Picard
            kwargs['lang'] = 'eng'

        self.mfile.tags.add(kls(text=str(md_val), **kwargs))

    def _ft_rmtag(self, key):
        self.mfile.tags.delall(key)


class Mp3File(Id3File):
    tag_format = "Mp3"
    mutagen_kls = mutagen.mp3.MP3

    def __init__(self, filename, **kwargs):
        super(Mp3File, self).__init__(filename, **kwargs)

        self.tag_map = self.tag_map.copy()
        self.tag_map.update({
            '#codec': TAG_MAP_ENTRY(getter=lambda afile, norm_key: 'mp3',
                                    type=str),
            '#bitspersample': TAG_MAP_ENTRY(getter=lambda afile, norm_key: None,
                                    type=int),
        })


class EasyMp3File(AudioFile):
    tag_format = "EasyMP3"
    mutagen_kls = mutagen.mp3.EasyMP3


class EasyId3File(AudioFile):
    tag_format = "EasyID3"
    mutagen_kls = mutagen.easyid3.EasyID3FileType


class TrueAudioFile(Id3File):
    tag_format = "TrueAudio"
    mutagen_kls = mutagen.trueaudio.TrueAudio


class EasyTrueAudioFile(AudioFile):
    tag_format = "EasyTrueAudio"
    mutagen_kls = mutagen.trueaudio.EasyTrueAudio
