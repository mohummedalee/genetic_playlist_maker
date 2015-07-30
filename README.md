# Genetic Playlist Maker

Old code experimenting with genetic algorithms for bulding playlists from a given seed song. Each chromosome is a playlist. Each song in a playlist is described as a difference of its Mel Frequency Cepstral Coefficients (MFCCs) from the seed song.

This was meant to investigate if MFCCs could actually be used as a parameter for song similarity. I really didn't get to any conclusive results and didn't find time to work on this again.
Code is available here just for pointers. Please don't expect it to be perfect.

Directory Structure:
Put your music (16 bit wav) files in a folder called 'music' next to the main.py file.
The only dependency is Python Speech Features, which I've provided in the repository (features/).
