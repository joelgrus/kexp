"""scrape old playlists from the KEXP API"""

import gzip
import requests
import json
import datetime
import time
import argparse

from dateutil.parser import parse

parser = argparse.ArgumentParser(description='Scrape some playlists.')
parser.add_argument('--start', type=str, help='earliest scrape date', default='')
parser.add_argument('--end', type=str, help='latest scrape date', default='')
parser.add_argument('--output_dir', type=str, default='kexp')

URL = 'http://cache.kexp.org/cache/plays'

def make_url(date: datetime.date) -> str:
    """create the URL to get all the plays for a single date"""
    return "{}?startTime={}&endTime={}&channel=1".format(
        URL,
        date.isoformat(),
        (date + datetime.timedelta(days=1)).isoformat()
    )

def plays_for_date(date: datetime.date):
    """fetch all the plays for a single date"""
    url = make_url(date)
    response = requests.get(url)
    return response.json()['Plays']

def scrape_date(date: datetime.date, output_dir: str):
    plays = plays_for_date(date)
    # `plays` has a lot of repeated info, so we gzip the output files, which
    # gets them about 10x smaller. this probably isn't entirely necessary, but
    # I was running this on an ec2 instance without a lot of disk space.
    with gzip.open('{}/{}.txt.gz'.format(output_dir, date.isoformat()), 'w') as f:
        for play in plays:
            f.write(bytes(json.dumps(play) + "\n", 'utf-8'))

if __name__ == "__main__":
    args = parser.parse_args()

    dt = parse(args.start).date() if args.start else datetime.date(2001,1,1)
    end_dt = parse(args.end).date() if args.end else datetime.date.today()

    while dt <= end_dt:
        print("scraping {}".format(dt))
        scrape_date(dt, args.output_dir)
        dt += datetime.timedelta(days=1)
        time.sleep(2)
