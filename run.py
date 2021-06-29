import praw
import configparser
import schedule
import time


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
reddit_target_subreddit = config['REDDIT']['reddit_target_subreddit']
sleep_timer = int(config['SETTINGS']['sleep_timer'])

reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent='Submission muncher! (by u/impshum)',
                     username=reddit_user,
                     password=reddit_pass)


def muncher():
    c = 0
    for submission in reddit.subreddit(reddit_target_subreddit).new(limit=None):
        submission.mod.remove()
        c += 1
    print(f'Deleted {c} submissions')


def main():
    muncher()
    schedule.every(sleep_timer).minutes.do(muncher)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
