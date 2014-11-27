import pymysql
import os
import time
import csv

def mysql_import(con, cur, directory):
	t = 0
	for trajectory in os.listdir(directory):
		p = 0
		for plt in os.listdir(directory + "/" + trajectory + "/Trajectory"):
			with open(directory + "/" + trajectory + "/Trajectory/" + plt) as trace:
				l = -1
				points = []
				for line in csv.reader(trace):
					if l != -1:
						points.append((t, p, line[0], line[1], line[3], line[5], line[6]))
						l += 1
					elif len(line) == 1 and line[0] == "0":
						l = 0
				#print(points)
				cur.executemany("insert into points (day, trajectory, latitude, longitude, altitude, date, time) values (%s, %s, %s, %s, %s, %s, %s)", points)
				con.commit()
			print("trajectory:" + str(t) + ":" + str(p))
			p += 1
		#print("trajectory:" + str(t))
		t += 1
	return

def mysql_trajectory_point_count(con, cur, day, trajectory):
	cur.execute("select count(1) from points where day=%s and trajectory=%s", (day, trajectory,))
	results = cur.fetchall()
	for result in results:
		print(result)
	return

def mysql_day_point_count(con, cur, day):
	cur.execute("select count(1) from points where day=%s", (day,))
	results = cur.fetchall()
	for result in results:
		print(result)
	return

con = pymysql.connect(host="localhost", user="client", database="assignment4")
cur = con.cursor()

#mysql_import(con, cur, "Data")

average = 0
min = 999999999
max = 0

for i in range(0, 10):
	start = time.clock()
	mysql_trajectory_point_count(con, cur, 0, i)
	end = time.clock()

	diff = end - start

	if diff < min:
		min = diff
	if diff > max:
		max = diff
	
	average += diff

average /= 10

print(min)
print(max)
print(average)

for i in range(0, 10):
	start = time.clock()
	mysql_day_point_count(con, cur, i)
	end = time.clock()

	diff = end - start

	if diff < min:
		min = diff
	if diff > max:
		max = diff
	
	average += diff

average /= 10

print(min)
print(max)
print(average)
