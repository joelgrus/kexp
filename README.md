# KEXP

I downloaded about 15 years of KEXP playlists, extracted all the `(artist, song)`
pairs, and trained a LSTM on them. (rnn_size: 300, seq_length: 100)

First of all `scrape.py` uses the [KEXP Cache API](http://cache.kexp.org/cache/docs)
to download historical playlists one day at a time. These playlist blobs are huge
with lots of repeated information (e.g. a long description of KEXP that's part of
every song), and I was running this on an ec2 instance with a small disk, so it
writes the data out to `.txt.gz` files, one JSON song per line.

There's a lot of interesting things you could do with either sequences of playlists
or trends over time, but I was mostly interested in the distinct songs themselves,
so I wrote `process.py` to summarize (artist, title, count) into `song_counts.txt`.

There is some interesting exploratory data analysis there (see the notebooks),
but my main goal was to train a LSTM on `"{artist} - {title}"` data so that
I could make up fake artists and songs.

The file `kexp_1m.txt` is the output from using that trained LSTM to generate
1 million characters, which ends up being about 30,000 fake songs. Some of them
end up being fake songs for real bands:

```
$ cat kexp_1m.txt | egrep "^Talking Heads"
Talking Heads - Cars Kick 'n' Egg Power
Talking Heads - Left Over
Talking Heads - How The Balaccan
Talking Heads - Bound to the Tide
Talking Heads - The Forkin' Man
Talking Heads - Riverdales Were Right
Talking Heads - Luci
Talking Heads - Roses Africanes
Talking Heads - The River Dock About (Liketa Through It's On)
Talking Heads - Flip Darkness
```

But the more interesting ones end up being fake bands:

```
RIVIP - 7 Nightmares
Rinkstyles - We Will Reall (Remix)
John Smith Gosvay - Brad Elvis On Wereville
Flight Faker - Three Down Friends Nobody Die
Doris Ill - Harlem Heart For Living
Short Glasses And The Robins - The Chat Pace
Julian Placer - Dance Yes Me
Knip Ducklin - Roys and View
Rita Sex - Pure Go Blind Vibration
Benimend - Heart Is Gone
```

Admit it, if I told you these were real KEXP bands you'd believe me.
