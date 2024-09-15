import json
import yt_dlp
import re
from os import environ



import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri=environ["SPOTIPY_REDIRECT_URI"],
                                               scope="user-library-read"))

#raaar global variables
#raaar im a bad programmer
NA=0
success=0
known_albums=[]



def main():
    URL = 'https://music.youtube.com/playlist?list=PLciqDR73n0emWF1k5LVgEzeRYAAkDVpG9'
    FILE= 'out.txt'

    global NA,success,known_albums

    album_urls='todl.txt'
    known='known.txt'

    #iterate through known albums file and append to variable:
    with open(known) as f:
        for line in f:

            known.albums.append(tuple(line.split(',')))

    clear(album_urls)
    clear(FILE)
    ydl_opts = {'extract_flat': 'in_playlist',
    'fragment_retries': 10,
    'ignoreerrors': True,
    'postprocessors': [{'key': 'FFmpegConcat',
                        'only_multi_video': True,
                        'when': 'playlist'},{'actions': [(yt_dlp.postprocessor.metadataparser.MetadataParserPP.interpretter,
                                    'title',
                                    '%(artist)s - %(title)s')],
                        'key': 'MetadataParser',
                        'when': 'pre_process'}
                    ],
    'print_to_file': {'video': [('%(artist)s --- %(title)s',
                                FILE)]},
    'retries': 10}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)

    print(f"Wrote {URL} contents to {FILE}")

    f=open(FILE)
    songs=[]
    for line in f:
        print(re.split(r' --- ',line))
        artist,title=re.split(r' --- ',line)
        if artist!=remove_junk(artist):
            old=title
            title=remove_junk(artist)
            artist=remove_junk(old)
        if ((artist!='NA' and title!='NA') and (('cover' not in title.lower()) and ('cover' not in artist.lower()))):
            songs.append([artist,remove_junk(title)])
        else:
            NA+=1
    f.close()
    print("Running albums against known albums:")
    albums_to_output = []
    for artist,title in songs:
        results = sp.search(q="artist:" + artist + " track:" + title,type='track')['tracks']
        #print(results)

        if results['items'] != []:
            result=(results['items'][0]['artists'][0]['name'],results['items'][0]['album']['name'],results['items'][0]['album']['external_urls']['spotify'])
            if add_if_unknown(result[0:2]):
                albums_to_output.append(result[2])

        else:
            #attempt again, swapping the track title and artist
            results = sp.search(q="artist:" + title + " track:" + artist,type='track')['tracks']
            if results['items'] != []:
                result=(results['items'][0]['artists'][0]['name'],results['items'][0]['album']['name'],results['items'][0]['album']['external_urls']['spotify'])
                if add_if_unknown(result[0:2]):
                    albums_to_output.append(result[2])
            else:
                print(f'{artist} - {title} did not find an album, discarding.')
                NA+=1
    clear(FILE)
    f = open(FILE, 'w')
    print(f'writing found albums to {FILE}...')
    for album in known_albums:
        print(f"writing {album} to {FILE}")
        f.write(f"('{'\',\''.join(album)}')\n")
    f.close()
    with open(album_urls,'w') as f:
        for url in albums_to_output:
            print(f'Writing {url} to {album_urls}')
            f.write(f'{url}\n')
    print('Done!')
    print(f'{success} albums found and {NA} songs discarded.')

def add_if_unknown(result):
    global NA,success
    global known_albums
    NA = NA
    success = success
    if result not in known_albums:
        known_albums.append(result)
        print(f"Adding {result} to albums")
        success+=1
        return True
    else:
        print(f"{result} found in known albums, discarding.")
        NA+=1
        return False

def remove_junk(text):
    junks=[r'[\|\r\n\(\[\+~]',r'[LlOo][YyFf][RrFf][Ii][Cc]','HD',": THE MOVIE"]
    for junk in junks:
        while text != re.split(junk,text)[0]:
            text = re.split(junk,text)[0]
    return text

def clear(FILE):
    print(f"Clearing {FILE}...")
    open(FILE, 'w').close()

if __name__=="__main__":
    main()
