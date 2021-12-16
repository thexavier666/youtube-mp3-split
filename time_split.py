#!/usr/bin/env python3

import re
import sys
import csv
import subprocess as sp
import tempfile
import os

def get_time(csv_row):
    start_time = csv_row[0]

    return start_time

def get_song_file_name(song_name, song_track_id):

    return "%02d %s" % (song_track_id, song_name)
def get_end_of_mp3(mp3_file):

    path_to_temp = 'temp.mp3'
    try:
        os.remove(path_to_temp)
    except:
        pass
    completed_process = sp.run('ffmpeg -i "{}" -acodec copy "{}"'.format(mp3_file, path_to_temp),shell = True, capture_output = True)
    if (completed_process.returncode == 0):
        lines = completed_process.stderr.decode('utf-8').split("\n")
        for line in lines:
            if "time=" in line:
                matches = re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9]", line)
                #last match is the end time
                os.remove(path_to_temp)
                if len(m) > 0:
                    return matches[-1]
                else:
                    #should never hit this else
                    raise OSError("Could not determine length of mp3.")
        os.remove(path_to_temp)
        raise OSError("Could not determine length of mp3.")
            
    else:
        os.remove(path_to_temp)
        raise OSError("Could not determine length of mp3.")
    
def make_songs(main_song_file, start_time, end_time, song_track_id, song_name, song_artist, song_album):
    
    song_file_name = get_song_file_name(song_name, song_track_id)
    meta_track_id = "%02d" % song_track_id

    str_cmd =("ffmpeg "
            "-loglevel -8 "
            "-i %s "
            "-acodec copy "
            "-metadata title=\"%s\" "
            "-metadata artist=\"%s\" "
            "-metadata album=\"%s\" "
            "-metadata track=\"%s\" "
            "-ss %s "
            "-to %s \"%s.mp3\"") % (main_song_file, song_name, song_artist, song_album, meta_track_id, start_time, end_time, song_file_name)

    sp.call(str_cmd, shell = True)
def processDoubleDash():
    for arg in sys.argv:
        if "--" in arg:
            if arg == "--help":
                print ("Arguments are \"song details\", \"big .mp3 file\"")
                exit(0)
def processDash():
    #processes required data
    termsToValues = None
    try:
        termsToValues = {"Song Details":sys.argv[1], "MP3":sys.argv[2]}
    except IndexError:
        print("Use necessary positional arguments song details and mp3 file")
        exit(-2)
    #processes optional data
    index = 0
    skipNext = False
    try:
        for i in range(3, len(sys.argv)):
            index = i
            if skipNext:
                skipNext = False
                continue
            if "-" is sys.argv[i][0]:
                if sys.argv[i] == "-aa":
                    termsToValues["Author Name"] = sys.argv[i+1]
                    skipNext = True
                elif sys.argv[i] == "-al":
                    termsToValues["Album Name"] = sys.argv[i+1]
                    skipNext = True
                        
    except IndexError:
        print("Supply correct argument for {}".format(sys.argv[index]))
        exit(-2)
    return termsToValues
def main():
    processDoubleDash()
    arguments = processDash()
    song_details = arguments["Song Details"]
    main_mp3_file = arguments["MP3"]
    album_artist  = arguments.get("Author Name", "")
    album_name    = arguments.get("Album Name", "")

    # opening the CSV file
    fp = csv.reader(open(song_details, 'r'), delimiter='|')

    song_list = []

    # getting the details of the 1st song
    first_song_details = next(fp)
    time_start = get_time(first_song_details)
    song_name = first_song_details[1]

    # counter to add at the begining of the song name
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

    #creating the last song
    time_end = get_end_of_mp3(main_mp3_file)
    song_list.append([time_start, time_end, track_id, song_name])
    # creating all the songs
    for row in song_list:
        make_songs(main_mp3_file, row[0], row[1], row[2], row[3], album_artist, album_name)

        print("[INFO] Song name {} created".format(row[3]))

if __name__ == '__main__':
    main()
