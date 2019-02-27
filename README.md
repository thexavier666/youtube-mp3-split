# youtube-mp3-split
Split large mixtapes from Youtube by their timestamps

## Prerequisite

1. Python 2.7
2. FFMPEG
3. youtube-dl (Optional)

## How to use

The best way to use it would be to use the following sample

1. Download the `.mp3` of a Youtube video. The best way to download would be to use `youtube-dl`

	youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=aRh1cZbwc4M

2. Remove the spaces of the downloaded file. This can be easily fixed. Say the new name of the file is `big_file.mp3`
3. Copy the time stamp details from the "Details" section of the video or from the comments
4. **CRUCIAL PART** Create a time stamp file in a `.csv` file format with separator as `|`. I have supplied a sample time stamp file for the above URL. The name of the file is `song_list`
5. Move `big_file.mp3` and `time_split.py` in `sample_run`
6. Use my script

	python time_split.py song_list big_file.mp3 "Martin O'Donnell,Michael Salvatori" "Halo: Reach OST"

7. All `.mp3`s will be generated by `FFMPEG`







