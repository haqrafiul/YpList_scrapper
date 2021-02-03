''' Grab all the video details from a YouTube Playlist '''
# This works upto 100 videos on a playlist
# python 3.8.2
from googleapiclient.discovery import build
# pylint: disable = E1101
import yaml  # to convert json data into a python dictionary


def write_padded_video_details(id, title, published, views, likes, dislikes, duration):
    s.write("{:13}".format(id))
    s.write("{:70}".format(title))
    s.write("{:22}".format(published))
    s.write("{:10}".format(views))
    s.write("{:6}".format(likes))
    s.write("{:6}".format(dislikes))
    s.write("{:10}".format(duration) + '\n')


if __name__ == '__main__':
    api_key = '--your key--'

    playlist_id = 'PL..'

    youtube = build('youtube', 'v3', developerKey=api_key)

    # part1

    request = youtube.playlistItems().list(part='contentDetails', maxResults=50,
                                           playlistId=playlist_id)
    response = request.execute()
    token = response.get('nextPageToken')

    if token is not None:
        request2 = youtube.playlistItems().list(part='contentDetails', maxResults=50,
                                                playlistId=playlist_id, pageToken=token)
        response2 = request2.execute()
        with open('ylist2.txt', 'w') as f2:  # Erase all contents
            pass
        with open('ylist2.txt', 'a') as f2:
            f2.write(str(response2))

    # # Erase all contents
    with open('ylist.txt', 'w') as f:
        pass

    with open('ylist.txt', 'a') as f:
        f.write(str(response))

    print('Done')

    # # Part 2

    video_ids = []

    with open('ylist.txt', 'r') as f3:
        f3 = f3.read()
        f3 = yaml.load(f3, Loader=yaml.CLoader)
        listy = f3.get('items')
        for x in range(0, len(listy)):
            y = listy[x].get('contentDetails').get('videoId')
            video_ids.append(y)

    if token is not None:
        with open('ylist2.txt', 'r') as f3:
            f3 = f3.read()
            f3 = yaml.load(f3, Loader=yaml.CLoader)
            listy = f3.get('items')
            for x in range(0, len(listy)):
                y = listy[x].get('contentDetails').get('videoId')
                video_ids.append(y)

    print('A-OK')

    # # Part 3

    # write the headings
    with open('stats.txt', 'w') as s:
        write_padded_video_details('ID', 'Title', 'Published', 'Views', 'Likes', 'Dislikes', 'Duration')

    for z in range(0, len(video_ids)):
        v_id = video_ids[z]
        request = youtube.videos().list(part='statistics', id=v_id)
        test = request.execute()
        r = test.get('items')[0].get('statistics')
        view = r.get('viewCount')
        like = r.get('likeCount')
        dislike = r.get('dislikeCount')

        request3 = youtube.videos().list(part="snippet", id=v_id)
        uu = request3.execute()
        title = uu.get('items')[0].get('snippet').get('title')
        date_published = uu.get('items')[0].get('snippet').get('publishedAt')

        requestT = youtube.videos().list(part="contentDetails", id=v_id)
        responseT = requestT.execute()
        with open('json.txt', 'w') as qt:
            qt = qt.write(str(responseT))
        with open('json.txt', 'r') as qq:
            qq = qq.read()
            qq = yaml.load(qq, Loader=yaml.CLoader)
            duration = qq.get('items')[0].get('contentDetails').get('duration')

        with open('stats.txt', 'a') as s:
            if like is None:
                like = "0"
            if dislike is None:
                dislike = "0"

            write_padded_video_details(v_id, title, date_published, view, like, dislike, duration)

    print('All Done')
