from tqdm import tqdm
from time import sleep
import re, requests
from youtube_transcript_api import YouTubeTranscriptApi
from tractor_beam.utils.globals import _f

class Helpers:
    def __init__(self, job):
        self.job = job
        self.data = []  # To keep track of fetched transcripts
    
    def process(self, transcript_data):
        progress_bar = tqdm(transcript_data, desc="Processing transcripts")
        for transcript in progress_bar:
            sleep(0.25)  # Just throttling
            try:
                isYT = re.search(r"(youtu.be)|(youtube.com)", self.job["url"])
                if isYT:
                    prefix = re.search("(?s:.*)/", self.job["url"])
                    YTID = self.job["url"][prefix.span()[1]:].replace("watch?v=", "") if prefix else None
                    _f("INFO", f'{self.job["url"]} has YouTube ID {YTID}')
                    youtubeTranscriptResult = YouTubeTranscriptApi.get_transcript(YTID, languages=['en'])
                    youtubeScript = self.format_transcript(youtubeTranscriptResult)
                    self.data.append({"id": YTID, "transcript": youtubeScript})
            except Exception as e:
                _f('fatal', f"Error fetching YouTube transcript for ID {YTID}: {e}")
            progress_bar.set_postfix({"transcripts processed": len(self.data)})
        return self.data

    def format_transcript(self, transcript):
        formatted_text = ""
        for item in transcript:
            line = item['text']
            formatted_text += line + "\n"
        return formatted_text

class Stream:
    def __init__(self, conf: str | dict = None, job: str | dict = None):
        self.job = job
        self.conf = conf
        self.helpers = Helpers(self.job)

    def fetch(self):
        transcript_data = [self.job['url']]
        processed_data = self.helpers.process(transcript_data)
        return processed_data

    def run(self):
        transcripts = self.fetch()
        return transcripts
