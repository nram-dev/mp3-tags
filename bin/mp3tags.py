#!/usr/local/bin/python3
# mp3tags.py
# dict_keys(['album', 'bpm', 'compilation', 'composer', 'copyright', 'encodedby', 'lyricist', 'length', 'media', 'mood', 'title', 'version', 'artist', 'albumartist', 'conductor', 'arranger', 'discnumber', 'organization', 'tracknumber', 'author', 'albumartistsort', 'albumsort', 'composersort', 'artistsort', 'titlesort', 'isrc', 'discsubtitle', 'language', 'genre', 'date', 'originaldate', 'performer:*', 'musicbrainz_trackid', 'website', 'replaygain_*_gain', 'replaygain_*_peak', 'musicbrainz_artistid', 'musicbrainz_albumid', 'musicbrainz_albumartistid', 'musicbrainz_trmid', 'musicip_puid', 'musicip_fingerprint', 'musicbrainz_albumstatus', 'musicbrainz_albumtype', 'releasecountry', 'musicbrainz_discid', 'asin', 'performer', 'barcode', 'catalognumber', 'musicbrainz_releasetrackid', 'musicbrainz_releasegroupid', 'musicbrainz_workid', 'acoustid_fingerprint', 'acoustid_id'])
# following tags are modified:
# - album
# - artist
# - tracknumber
# - composer
# - genre
# USAGE
# python3 bin/mp3tags.py --dir /path/to/music/library

import sys, os
import argparse
import pprint
from pathlib import Path
import glob
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import yaml

me = "mp3tags.py"

# read tags from TAGS.yaml file
# format:
# albuminfo:
#   album: name
#   artist: name
#   composer: name
#   genre: info
# trackinfo:
#   - "track 1.mp3"
#   - "track 2.mp3"
#   - ...
#
def read_tags_yaml(tagsfile):
    print ("Reading tagsfile :", tagsfile)
    with open(tagsfile) as f:
        tags = yaml.load(f)
        print(tags)
        return tags['albuminfo'], tags['trackinfo']

# Parse dir in the form of /some/path/Artist/Album/filename
# extrct an return Album & Artist
# note: not used
def parse_dir(file):
    print ("Parsing file :", file)
    p1, f = os.path.split(file)
    p1,album = os.path.split(p1)
    p1,artist = os.path.split(p1)
    print ("   Album: {} Artist: {}".format(album, artist))
    return album, artist

# get list of mp3 files from dir
# note: not used, dir list used from trackinfo in yaml
#       this doesn't guarantee order for tracknumber 
def glob_dir(dir):
    print ("Globbing dir: ", dir)
    files=dir.glob('**/*.mp3')
    print ("Files: ", files)
    return files

# main
def main(argv):
    p = argparse.ArgumentParser( prog=me,
   	description= me + ": Read and Edit MP3 Tags",
        formatter_class=argparse.RawDescriptionHelpFormatter)   
    # Required args
    pr = p.add_argument_group("Required")
    pr.add_argument('--dir',  action="store", dest='dir', required=True, help='Directory with mp3 files')
    # Optional args
    po = p.add_argument_group("Optional")
    po.add_argument('--tags', dest="tagsfile", default="TAGS.yaml", help='TAGS file')
    #po.add_argument("--list",  action="store_true" , default=True,help="List tags")
    #po.add_argument("--edit",  action="store_true" , default=False,help="Edit tags")
    po.add_argument('--verbose', '-v', action="count", default=0, help='Verbose mode: -v verbose, -vv debug, -vvv trace')

    r = p.parse_args()

    if r.verbose > 0:
        print(EasyID3.valid_keys.keys())

    albuminfo, trackinfo = read_tags_yaml("{}/{}".format(r.dir,r.tagsfile))

    print ("Scaning dir {}".format(r.dir))
    #d = Path(r.dir)
    n = 1
    for fname in trackinfo:
        file="{}/{}".format(r.dir, fname)
        print ("- file: {}".format(file))
        mt = EasyID3(file)
        for t in albuminfo.keys():
            mt[t] = albuminfo[t]
        mt['tracknumber'] = "{}".format(n)
        mt.save()
        #mt.pprint()
        n=n+1
        #print(mt.info.pprint)
        #tags=mutagen.File(file).keys()
        #pprint(tags)

if __name__ == "__main__":
    main(sys.argv[1:])