#provider for retrieving code reviews from gerrit
#makes use of https://github.com/shanesmith/gerrit-sh
#to provide a simpler interface on top of the gerrit-ssh API
import json
import redis
import time
import subprocess
from datetime import datetime

channel_name = 'scoreboard'

#relies on this gerrit-sh config existing already
gerrit_ssh_config = ''

project = None
if project:
    gerrit_cmd = "gerrit ssh %s \"query --format=JSON --comments 'status:open limit:15 project:%s'\"" % (gerrit_ssh_config,project)
else:
    gerrit_cmd = "gerrit ssh %s \"query --format=JSON --comments 'status:open limit:15'\"" % (gerrit_ssh_config)
def main():
    r = redis.Redis()
    while True:
        print gerrit_cmd
        sub_process = subprocess.Popen(gerrit_cmd, stdout=subprocess.PIPE,shell=True)
        output = sub_process.communicate()[0]
        reviews = output.split('\n')
        msgs = []
        #the slice is a hack, I know from experimentation
        #I can drop the last 2 as they aren't reviews
        for review_as_string in reviews[0:len(reviews)-2]:
            review = json.loads(review_as_string)
            project = review['project']
            author = review['owner']['name']
            subject = review['subject']
            msg_for_commit = "%s submitted %s to %s" % (author,subject,project)
            msgs.append(msg_for_commit)
            if 'comments' in review:
                comments = review['comments']
                msgs.append("Comment(s):")
                for comment in comments:
                    reviewer = comment['reviewer']['name']
                    message = comment['message'].replace('\n\n','. ')
                    msg_for_review = "%s says: %s" % (reviewer,message)
                    msgs.append(msg_for_review)
        data_for_board = json.dumps({'provider':'gerrit','messages':msgs,'append':False})
        r.publish(channel_name,data_for_board)
        time.sleep(1*15*60) #update every 15 minutes
     



if __name__ == '__main__':
    main()
