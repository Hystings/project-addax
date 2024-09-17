from ytmusicapi import YTMusic
ytm = YTMusic()

class bcolors:
	GREEN = '\033[92m'
	CYAN = '\033[96m'
	PINK = '\033[35m'
	ENDC = '\033[0m'
	RED = '\033[31m'


def main():
	album_list = []
	yt_playlists=[]
	output_file='youtube playlists.txt'
	with open('out.txt') as f:
		for line in f:
			#removes the '(...) ' from text
			line = line[1:-2]
			#turns line into a list, appends to album list 
			line = line.split(',')
			if len(line) > 2:
				line = [line[0],''.join(line[1:])]
			album_list.append(line)
			
			
	in_count = len(album_list)	
			
	
	for artist,title in album_list:
		
		
		yt_playlist=ytm.search(f"{artist} - {title}","albums")
		if yt_playlist != []:
			yt_playlist = yt_playlist[0]
			print(f'{bcolors.GREEN+artist+bcolors.ENDC} - {bcolors.PINK+title+bcolors.ENDC} returned {bcolors.CYAN+yt_playlist['playlistId']+bcolors.ENDC}, ({bcolors.GREEN+yt_playlist['artists'][0]['name']+bcolors.ENDC} - {bcolors.PINK+yt_playlist['title']+bcolors.ENDC}), appending to list')
			yt_playlists.append(f'https://music.youtube.com/playlist?list={yt_playlist['playlistId']}')
		else:
			print(f'{bcolors.RED+artist+bcolors.ENDC} - {bcolors.RED+title+bcolors.ENDC} did not find a playlist that matched, Discarding!')
			
	out_count = len(yt_playlists)
	with open(output_file, 'w') as f:
		for yt_playlist in yt_playlists:
			print(f'writing {yt_playlist} to {output_file}')
			f.write(f'{yt_playlist}\n')
	print(f'Done!\nFound {out_count} out of {in_count} searches.')


	
	
	


if __name__=="__main__":
	main()