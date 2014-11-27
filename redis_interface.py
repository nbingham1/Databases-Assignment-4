import redis
import csv
import os
import time

def redis_import(store, directory):
	t = 0
	for trajectory in os.listdir(directory):
		p = 0
		for plt in os.listdir(directory + "/" + trajectory + "/Trajectory"):
			with open(directory + "/" + trajectory + "/Trajectory/" + plt) as trace:
				l = -1
				for line in csv.reader(trace):
					if l != -1:
						store.set("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":latitude", line[0]);
						store.set("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":longitude", line[1]);
						store.set("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":altitude", line[3]);
						store.set("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":date", line[5]);
						store.set("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":time", line[6]);
						store.sadd("trajectory:" + str(t) + ":" + str(p) + ":points", "trajectory:" + str(t) + ":" + str(p) + ":" + str(l))
						store.sadd("trajectory:" + str(t) + ":points", "trajectory:" + str(t) + ":" + str(p) + ":" + str(l))
						#print("trajectory:" + str(t) + ":" + str(p) + ":" + str(l) + ":\t" + str(line))
						l += 1
					elif len(line) == 1 and line[0] == "0":
						l = 0
			print("trajectory:" + str(t) + ":" + str(p))
			p += 1
		#print("trajectory:" + str(t))
		t += 1	

def redis_trajectory_point_count(store, key):
	print(store.scard(key + ":points"))

def redis_day_point_count(store, key):
	print(store.scard(key + ":points"))

r = redis.StrictRedis()

#redis_import(r, "Data")

min = 9999999999
max = 0
average = 0

for i in range(0, 10):
	start = time.clock()	
	redis_trajectory_point_count(r, "trajectory:0:" + str(i))
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

min = 9999999999
max = 0
average = 0

for i in range(0, 10):
	start = time.clock()
	redis_day_point_count(r, "trajectory:" + str(i))
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
