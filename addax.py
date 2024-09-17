import json
import re
from os import environ,path
from sys import argv

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

class bcolors:
	GREEN = '\033[92m'
	CYAN = '\033[96m'
	PINK = '\033[35m'
	ENDC = '\033[0m'
	RED = '\033[31m'

def add_color(text, color_to_add=bcolors.GREEN):
    return color_to_add+text+bcolors.ENDC
    

ytm = YTMusic()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=environ["SPOTIPY_CLIENT_ID"],
                                               client_secret=environ["SPOTIPY_CLIENT_SECRET"],
                                               redirect_uri=environ["SPOTIPY_REDIRECT_URI"],
                                               scope="user-library-read"))

#raaar global variables
#raaar im a bad programmer
NA=0
duplicates=0
success=0
known_albums=[]

def main():
    FILE= 'out.txt'

    if len(argv) > 2:
        print("usage: python addax.py [Playlist URL]")
    elif len(argv) == 1:
        URL = 'https://music.youtube.com/playlist?list=PLciqDR73n0emWF1k5LVgEzeRYAAkDVpG9'
        print(f'No album input, using default of {add_color(URL,bcolors.CYAN)}.') 
    else:
        URL = argv[1]
    
    global NA,success,known_albums,duplicates

    album_urls='todl.txt'
    known='known.txt'

    #iterate through known albums file and append to variable:
    if path.exists(known):
        with open(known) as f:
            for line in f:
                known.albums.append(tuple(line.split(',')))

    clear(album_urls)
    songs=ytm.get_playlist(url_to_list_id(URL),None)['tracks']
    
    
    
    albums_to_output=[]
    
    for song in songs:
        artist,title=song['artists'][0]['name'],song['title']
        results = sp.search(q="artist:" + artist + " track:" + remove_junk(title),type='track')['tracks']

        if results['items'] != []:
            result=(results['items'][0]['artists'][0]['name'],results['items'][0]['album']['name'],results['items'][0]['album']['external_urls']['spotify'])
            if add_if_unknown(result[0:2]):
                albums_to_output.append(result[2])
        else:
            #attempt again, this time attempting to remove the youtube channel from the artist:
            results = sp.search(q="artist:" + "".join(artist.split('-')[1:]) + " track:" + remove_junk(title),type='track')['tracks']
            if results['items'] != []:
                result=(results['items'][0]['artists'][0]['name'],results['items'][0]['album']['name'],results['items'][0]['album']['external_urls']['spotify'])
                if add_if_unknown(result[0:2]):
                    albums_to_output.append(result[2])
            else:
                print(f'{add_color(artist,bcolors.RED)} - {add_color(remove_junk(title),bcolors.RED)} did not find an album, discarding.')
                NA+=1
    clear(FILE)
    f = open(FILE, 'w')
    print(f'writing found albums to {FILE}...')
    for album in known_albums:
        print(f"writing {add_color(album[0])} - {add_color(album[1],bcolors.PINK)} to {FILE}")
        f.write(f"('{'\',\''.join(album)}')\n")
    f.close()
    with open(album_urls,'w') as f:
        for url in albums_to_output:
            print(f'Writing {add_color(url,bcolors.CYAN)} to {album_urls}')
            f.write(f'{url}\n')
    print('Done!')
    print(f'{success+duplicates} songs successfully parsed, {success} albums found, {duplicates} duplicate albums and and {NA} unable to find songs discarded.')

def add_if_unknown(result):
    global duplicates,success
    success = success
    if result not in known_albums:
        known_albums.append(result)
        print(f"Adding {add_color(result[0])}, {add_color(result[1],bcolors.PINK)} to albums")
        success+=1
        return True
    else:
        print(f"{add_color(','.join(result),bcolors.RED)} found in known albums, discarding.")
        duplicates+=1
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

def url_to_list_id(URL):
    if URL.split('?list=')[-1]!=URL:
        return URL.split('?list=')[-1]
    else:
        return URL.split('&list=')[-1]

if __name__=="__main__":
    main()