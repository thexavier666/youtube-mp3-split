import sys
import csv
import subprocess as sp

def get_time(csv_row):
	start_time = csv_row[0]

	return start_time

def get_song_file_name(song_name, song_track_id):

	return "%02d %s" % (song_track_id, song_name)

def make_songs(main_song_file, start_time, end_time, song_track_id, song_name, song_artist, song_album):

	song_file_name = get_song_file_name(song_name, song_track_id)
	meta_track_id = "%02d" % song_track_id

	str_cmd =("ffmpeg "
			"-i %s "
			"-acodec copy "
			"-metadata title=\"%s\" "
			"-metadata artist=\"%s\" "
			"-metadata album=\"%s\" "
			"-metadata track=\"%s\" "
			"-ss %s "
			"-to %s \"%s.mp3\"") % (main_song_file, song_name, song_artist, song_album, meta_track_id, start_time, end_time, song_file_name)

	print str_cmd

	sp.call(str_cmd, shell = True)

def main():

	if len(sys.argv) < 4:
		print "Arguments are \"song details\", \"big .mp3 file\", \"album artist\", \"album name\""
		return 1

	song_details  = sys.argv[1]
	main_mp3_file = sys.argv[2]
	album_artist  = sys.argv[3]
	album_name    = sys.argv[4]

	# opening the CSV file
	fp = csv.reader(open(song_details, 'r'), delimiter='|')

	song_list = []

	# getting the details of the 1st song
	first_song_details = fp.next()

	time_start = get_time(first_song_details)
	song_name = first_song_details[1]

	# counter to add at the beggining of the song name
	track_id = 1

	for row in fp:
		# getting the start time of the next song
		# which will be the end time of the current song
		next_song_start = get_time(row)

		time_end = next_song_start

		# creating the song name and removing leading spaces
		song_name = "%s" % (song_name.strip())

		song_list.append([time_start, time_end, track_id, song_name])

		# next song's name
		song_name = row[-1]

		# next song's track ID
		track_id += 1

		# next song's start time
		time_start = time_end

	# creating all the songs
	for row in song_list:
		make_songs(main_mp3_file, row[0], row[1], row[2], row[3], album_artist, album_name)
		

if __name__ == '__main__':
	main()
