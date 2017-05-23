from collections import Counter
import csv
import json
import glob
import gzip
from typing import NamedTuple, List
import argparse

parser = argparse.ArgumentParser(description='Process some scraped playlists.')
parser.add_argument('--data_glob', type=str, default = 'kexp/*.txt.gz')
parser.add_argument('--output', type=str, default='songs.txt')

Song = NamedTuple('Song', [('artist', str), ('title', str)])

def songs_from_file(fn: str) -> List[Song]:
    print("reading songs from {}".format(fn))
    with gzip.open(fn) as f:
        lines = [line.decode() for line in f]
        tracks = [json.loads(line) for line in lines]
        # only tracks with artist and title

        return [
            Song(track['Artist']['Name'].strip(), track['Track']['Name'].strip())
            for track in tracks
            if track['Artist'] is not None and track['Track'] is not None
        ]

if __name__ == "__main__":
    args = parser.parse_args()

    songs = [
        song
        for fn in glob.glob(args.data_glob)
        for song in songs_from_file(fn)
    ]

    play_counts = Counter(songs)

    with open(args.output, 'w') as f:
        writer = csv.writer(f)
        for song, count in play_counts.items():
            writer.writerow([song.artist, song.title, count])
