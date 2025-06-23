make sure you update the location of the "compress_video.py" script in "runner.bat"!

to add to winreg:
	windows -> regedit
	Computer\HKEY_CLASSES_ROOT\SystemFileAssociations\.mp4\shell\Compress Video\command
								this will be what shows
								up in the context menu!
	command: "C:\Scripts\compress_video\runner.bat" "%1"
	where the first path points to the batch file, and %1 indicates the file that is being
	passed by the context menu
	
this works by calculating the maximum bitrate to get the file size to <10mb, and then also reducing resolution. sometimes it doesn't get to under 10 mb, just compress again :P