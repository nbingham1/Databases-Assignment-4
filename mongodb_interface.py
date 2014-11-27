from pymongo import MongoClient
import os
import csv
import time

def mongo_import(store, directory):
	t = 0
	for trajectory in os.listdir(directory):
		p = 0
		for plt in os.listdir(directory + "/" + trajectory + "/Trajectory"):
			with open(directory + "/" + trajectory + "/Trajectory/" + plt) as trace:
				l = -1
				for line in csv.reader(trace):
					if l != -1:
						point = {"day" : t, "trajectory" : p, "latitude" : line[0], "longitude" : line[1], "altitude" : line[3], "date" : line[5], "time" : line[6]}
						store.insert(point)
						l += 1
					elif len(line) == 1 and line[0] == "0":
						l = 0
			
			print("trajectory:" + str(t) + ":" + str(p))
			p += 1
		#print("trajectory:" + str(t))
		t += 1
	return

def mongo_trajectory_point_count(store, day, trajectory):
	print(store.find({"day" : day, "trajectory" : trajectory}).count())
	return

def mongo_day_point_count(store, day):
	print(store.find({"day" : day}).count())
	return

client = MongoClient()

db = client['assignment4']
collection = db['gps_trace']

#mongo_import(collection, "Data")

average = 0
min = 99999999
max = 0

for i in range(0, 10):
	start = time.clock()
	mongo_trajectory_point_count(collection, 0, i)
	end = time.clock()

	diff = end - start
	
	if min > diff:
		min = diff
	if max < diff:
		max = diff
	
	average += diff

average /= 10

print(min)
print(max)
print(average)

for i in range(0, 10):
	start = time.clock()
	mongo_day_point_count(collection, i)
	end = time.clock()

	diff = end - start

	if min > diff:
		min = diff
	if max < diff:
		max = diff
	
	average += diff

average /= 10

print(min)
print(max)
print(average)

