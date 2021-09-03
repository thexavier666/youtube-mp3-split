# youtube-mp3-split
Split large mixtapes from Youtube by their timestamps

## Prerequisite

1. Python 3.6
2. `ffmpeg`
3. `youtube-dl` (Optional)

## How to use

The best way to use it would be to use the following sample

1. Download the `.mp3` of a Youtube video. The best way to download would be to use `youtube-dl`

	`youtube-dl --extract-audio --audio-format mp3 https://www.youtube.com/watch?v=0QKQlf8r7ls`

2. Remove the spaces of the downloaded file. This can be easily fixed. Say the new name of the downloaded file is `big_file.mp3`
3. Copy the time stamp details from the "Details" section of the video or from the comments
4. **CRUCIAL PART**
	* Create a time stamp file in a `.csv` file format with separator as `|`
	* I have supplied a sample time stamp file for the above URL. The name of the file is `song_list.csv`
	* Make sure to create a NULL row as shown in the sample file. The NULL row denotes when the song ends.
	* If you don't create this row, the last song won't be created.
5. Use the following command

	`python3 time_split.py song_list.csv big_file.mp3 "Marvel83" "Back To The 80s - Best of Synthwave And Retro Electro Music Mix"`

6. All `.mp3`s will be generated in the current directory

PS: If your song does not have a singular artist or the songs belong to different albums, then put empty arguments inside double quotes.

## Disclaimer

This is a very basic first attempt at creating such a script. There might be bugs and un-handled exceptions `;_;`
