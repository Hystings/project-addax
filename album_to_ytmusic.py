from ytmusicapi import YTMusic
ytm = YTMusic()




def main():
	album_list = []
	yt_playlists=[]
	output_file='youtube playlists.txt'
	with open('out.txt') as f:
		for line in f:
			#removes the '(...) ' from text
			line = line[1:-2]
			#turns line into a list, appends to album list 
			album_list.append(line.split(','))
			
	in_count = len(album_list)	
			
	
	for album in album_list:
		yt_playlist=ytm.search(f"{album[0]} - {album[1]}","albums")[0]['playlistId']
		print(f'{album[0]} - {album[1]} returned {yt_playlist}, appending to list')
		yt_playlists.append(f'https://music.youtube.com/playlist?list={yt_playlist}')
	out_count = len(yt_playlists)
	with open(output_file, 'w') as f:
		for yt_playlist in yt_playlists:
			print(f'writing {yt_playlist} to {output_file}')
			f.write(f'{yt_playlist}\n')
	print(f'Done!\nFound {out_count} out of {in_count} searches.')


	
	
	


if __name__=="__main__":
	main()