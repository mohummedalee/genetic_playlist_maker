#from __future__ import division
import numpy
import sys
from numpy import *
import scipy
from features import mfcc
from features import fbank
import scipy.io.wavfile as wav
import os
import glob
from scipy.io import wavfile
import math
import random
import copy

#---------------------GLOBAL STUFF------------------------

os.chdir("music/")

seed = "lean_on.wav"
all_songs = []
all_playlists = []

#---------------------CLASSES------------------------

class Song:
	#Fields: name, difference_vector
	def __init__(self, name):
		self.name = name
		(rate, sig) = wav.read(self.name)
		my_mfcc = reduce_matrix(mfcc(sig, rate), 500)
		diff = subtract_mfcs(my_mfcc, seed_mfcc)
		self.difference_vector = difference_vector(diff)
		#self.used = false;
		#Add fitness points
		self.points = 0
		for score in self.difference_vector:
			if -2 <= score <= 2:
				self.points += 20
			elif -10 <= score <= 10:
				self.points += 7
			elif -40 <= score <= 40:
				self.points += 5
			elif -60 <= score <= 60:
				self.points += 3
			elif -100 <= score <= 100:
				self.points += 1

class Playlist:

    def calc_fitness(self):
    	fitness = 0

    	for song in self.songs:
    		print "song: ", song.name
    		fitness += song.points

    	return fitness

    def randomize(self):
    	while len(self.songs) < self.length:
	    	current_song = all_songs[random.randint(0, len(all_songs)-1)]
	    	self.songs.append(Song(current_song))
	    	#Remove so never added to any other playlist
	    	all_songs.remove(current_song)

        self.fitness = self.calc_fitness()

    def __init__(self, size):
    	#Pick size random songs from all_songs
    	self.songs = []
    	self.length = size
    	all_playlists.append(self)

    def add(self, song):
    	self.songs.append(song)
    	self.fitness = self.calc_fitness()
    	print "child new fitness: ", self.fitness


#---------------------FUNCTIONS------------------------
def holocaust():
	global all_playlists
	total = 0

	for i in all_playlists:
		total+= i.fitness

	avg = total/(len(all_playlists))

	for i in all_playlists:
		if i.fitness < avg:
			all_playlists.remove(i)



def subtract_mfcs(mfcc1, mfcc2):
	length = min(len(mfcc1), len(mfcc2))
	length -= 1
	ret = []
	found = 0;
	for i in range(length):
		feat_vec = []
		found = 0
		for j in range(13):
			if math.isnan(mfcc1[i][j]) or math.isnan(mfcc2[i][j]):
				found = 1
				break
			else:
				feat_vec.append(abs(mfcc1[i][j] - mfcc2[i][j]))
		if found == 0:
			ret.append(feat_vec)

	return ret

def reduce_matrix(mat, size):
	#Reduces the matrix to size number of rows
	jump = math.floor(len(mat)/size)
	row = 0
	ret = []

	while row < len(mat) and len(ret) < size:
		#Add this row to final
		ret.append(mat[row])
		#Take jump
		row += jump


	return ret

def get_13_chunk(mat, start, end):
	ret = []

	while start < end:
		ret.append(mat[start])
		start += 1

	return ret

def difference_vector(mat):
	#Splits the MFCC difference matrix into 30 (13x13) matrices and returns a vector of their determinants
	count = 0
	ret = []
	start = 0

	while count < 30:
		chunk = get_13_chunk(mat, start, start+13)
		ret.append(numpy.linalg.det(chunk))
		start += 13
		count += 1

	#Threshold values
	thresholded = [val/10000000000000 for val in ret]
	return thresholded

def start(seed):
	#Prepare global variables and the seed_mfcc
	(rate, sig) = wav.read(seed)
	for file in glob.glob("*.wav"):
		all_songs.append(file)

	woteva = mfcc(sig, rate)
	woteva = reduce_matrix(woteva, 500)
	return woteva

def generate_population(pop_size, playlist_size):
	global all_playlists

	for i in range(pop_size):
		x = Playlist(playlist_size)
		x.randomize()


def crossover(playlist_1, playlist_2, playlist_size):
	#Crosses over playlists
	global all_playlistsl
	#print "Playlist_size: ", playlist_size
	one = all_playlists[playlist_1]
	two = all_playlists[playlist_2]

	child = Playlist(playlist_size)

	one_percentage = (one.fitness / float(one.fitness + two.fitness))
	#print "One %: ", one_percentage
	one_genes = int(floor(playlist_size * one_percentage))
	print "One genes: ", one_genes

	one_copy = copy.deepcopy(one)
	two_copy = copy.deepcopy(two)

	#Get genes from first parent
	for i in range(one_genes):
		#if len(one_copy.songs) <= 1:
		#	two_genes+=1
		#	break
		all_songs.append(file)

	woteva = mfcc(sig, rate)
	woteva = reduce_matrix(woteva, 500)
	return woteva

def generate_population(pop_size, playlist_size):
	global all_playlists

	for i in range(pop_size):
		x = Playlist(playlist_size)
		x.randomize()

def exists_in_child(playlist, song):
	for i in playlist:
		if i.name == song.name:
			return True
	return False

def mutate(playlist):
	dice = random.randint(0, 200)
	if 50 <= dice <= 55:
		print "mutated"
		song = all_songs[random.randint(0, len(all_songs)-1)]
		all_songs.remove(song)
		playlist.songs[random.randint(0, len(playlist.songs)-1)] = Song(song)
	else:
		#No mutation
		return playlist

def crossover(playlist_1, playlist_2, playlist_size):
	#Crosses over playlists
	global all_playlists
	#print "Playlist_size: ", playlist_size
	one = all_playlists[playlist_1]
	two = all_playlists[playlist_2]

	child = Playlist(playlist_size)

	one_percentage = (one.fitness / float(one.fitness + two.fitness))
	#print "One %: ", one_percentage
	one_genes = int(floor(playlist_size * one_percentage))
	print "One genes: ", one_genes

	one_copy = copy.deepcopy(one)
	two_copy = copy.deepcopy(two)

	#Get genes from first parent
	for i in range(one_genes):
		pick = random.randint(0, len(one_copy.songs)-1)
		child.add(one_copy.songs[pick])
		one_copy.songs.remove(one_copy.songs[pick])
		#one_copy.length -= 1

	two_genes = int(playlist_size - one_genes)
	#print "Two genes: ", two_genes

	#Get genes from second parent
	for i in range(two_genes):
		pick = random.randint(0, len(two_copy.songs)-1)
		while exists_in_child(child.songs, two_copy.songs[pick]):
			print "hit"
			pick = random.randint(0, len(two_copy.songs)-1)
		child.add(two_copy.songs[pick])
		two_copy.songs.remove(two_copy.songs[pick])
		#two_copy.length -= 1

	child = mutate(child)

	#print "One fitness: ", one.fitness
	#print "Two fitness: ", two.fitness
	#print "Child fitness: ", child.fitness

def all_crossovers(size, crossover_count):
	for i in range(crossover_count):
		print i
		if crossover_count % 20 == 0:
			holocaust()
		crossover(random.randint(0, len(all_playlists)-1), random.randint(0, len(all_playlists)-1), size)

#------------------GLOBAL STUFF------------------------#
print "Calculating seed_mfcc..."
seed_mfcc = start(seed)

if __name__ == '__main__':
	#Make all_playlists
	playlist_size = 2
	pop_count = 4
	crossover_count = 50
	generate_population(pop_count, playlist_size)
	all_crossovers(playlist_size, crossover_count)

	#Call all crossovers
