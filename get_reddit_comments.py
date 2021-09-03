# a python function that accepts a reddit permalink and returns the comments


import praw
import pprint
import argparse


def get_comments(permalink):
    """
    get_comments(permalink)

    :param permalink: a reddit permalink to a thread
    :returns: a list of comments in the thread, each comment is a dict with keys 'body', 'author', 'created'
    """
    # create a praw instance
    r = praw.Reddit(user_agent='reddit-comment-downloader')

    # get the submission object
    submission = r.get_submission(permalink=permalink)

    # get the comments from the submission object
    submission.replace_more_comments(limit=None, threshold=0)
    flat_comments = praw.helpers.flatten_tree(submission.comments)

    # convert the comments into a list of dicts
    comments = []
    for comment in flat_comments:
        if isinstance(comment, praw.objects.MoreComments):
            continue
        comment_dict = {'body': comment.body, 'author': comment.author.name, 'created': comment.created}
        comments.append(comment_dict)

    return comments


def main():
    """
    main()

    :returns: None
    """
    # create an argument parser
    parser = argparse.ArgumentParser(description='A command line tool to download comments from reddit')

    # add the permalink argument
    parser.add_argument('permalink', help='the permalink of the thread to download comments from')

    # parse the arguments
    args = parser.parse_args()

    # get the comments
    comments = get_comments(args.permalink)

    # print the comments
    pprint.pprint(comments)


if __name__ == '__main__':
    main()