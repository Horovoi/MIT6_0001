# Problem Set 5: RSS Feed Filter
# Name: Mykyta Horovoi
# Collaborators: None

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.decription = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.decription

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def get_phrase(self):
        return self.phrase

    def is_phrase_in(self, text):
        text = text.lower()
        phrase = self.get_phrase().lower()

        for p in string.punctuation:
            text = text.replace(p, " ")

        text_list = text.split()
        phrase_list = phrase.split()

        if len(phrase_list) > len(text_list):
            return False
        else:
            for i in range(len(text_list) - len(phrase_list) + 1):
                if text_list[i:(i + len(phrase_list))] == phrase_list:
                    return True

            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        self.time = self.time.replace(tzinfo = pytz.timezone("EST"))

    def get_time(self):
        return self.time

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.timezone("EST")) < self.get_time()

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return story.get_pubdate().replace(tzinfo = pytz.timezone("EST")) > self.get_time()


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def get_trigger(self):
        return self.trigger

    def evaluate(self, story):
        return not self.get_trigger().evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def get_trigger1(self):
        return self.trigger1

    def get_trigger2(self):
        return self.trigger2

    def evaluate(self, story):
        return self.get_trigger1().evaluate(story) and self.get_trigger2().evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def get_trigger1(self):
        return self.trigger1

    def get_trigger2(self):
        return self.trigger2

    def evaluate(self, story):
        return self.get_trigger1().evaluate(story) or self.get_trigger2().evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    return_list = []

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                return_list.append(story)
                break
    
    return return_list


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    triggers_list = []
    return_list = []
    trigger_dict = {}

    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    for line in lines:
        triggers_list.append(line.split(","))

    for trigger in triggers_list:
        if trigger[1] == "TITLE":
            trigger_dict[trigger[0]] = TitleTrigger(trigger[2])
        elif trigger[1] == "DESCRIPTION":
            trigger_dict[trigger[0]] = DescriptionTrigger(trigger[2])
        elif trigger[1] == "AFTER":
            trigger_dict[trigger[0]] = AfterTrigger(trigger[2])
        elif trigger[1] == "BEFORE":
            trigger_dict[trigger[0]] = BeforeTrigger(trigger[2])
        elif trigger[1] == "NOT":
            trigger_dict[trigger[0]] = NotTrigger(trigger_dict[trigger[2]])
        elif trigger[1] == "AND":
            trigger_dict[trigger[0]] = AndTrigger(trigger_dict[trigger[2]], trigger_dict[trigger[3]])
        elif trigger[1] == "OR":
            trigger_dict[trigger[0]] = OrTrigger(trigger_dict[trigger[2]], trigger_dict[trigger[3]])
        elif trigger[0] == "ADD":
            for i in range(1, len(trigger)):
                return_list.append(trigger_dict[trigger[i]])
    
    return return_list
    

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Ukraine")
        t2 = DescriptionTrigger("GDP")
        t3 = DescriptionTrigger("Inflation")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News" # changed from "Google & Yahoo Top News" because Yahoo is no longer supported
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed

            # Update: Yahoo's RSS feed no longer includes descriptions,
            # so we can't use this line from the original code

            # stories.extend(process("http://news.yahoo.com/rss/topstories"))


            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()