import pymysql
import os
import time
import csv

def mysql_table_exists(con, cur, tablename):
	if cur.execute("show tables like '" + tablename + "'") > 0:
		return True
	else:
		return False

def mysql_import_trajectories(con, cur, directory):
	if mysql_table_exists(con, cur, "points"):
		cur.execute("drop table points")
		con.commit()
	
	cur.execute("create table points (day int, trajectory int, latitude double, longitude double, altitude double, date text, time text)")
	cur.commit()

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

def mysql_import_roadNet(con, cur, filename):
	if mysql_table_exists(con, cur, "edges"):
		cur.execute("drop table edges")
		con.commit()

	cur.execute("create table edges (`from` int, `to` int)")
	con.commit()

	i = 0
	with open(filename) as tsv:
		edges = []
		for line in csv.reader(tsv, delimiter="\t"):
			if len(line) >= 2 and len(line[0]) > 0 and line[0][0] != '#':
				edges.append((line[0], line[1],))
			i += 1

			if i >= 10000:
				cur.executemany("insert into edges (`from`, `to`) values(%s, %s)", edges)
				con.commit()

				if mysql_table_exists(con, cur, "nodes"):
					cur.execute("drop table nodes")
					con.commit()

				cur.execute("create table `nodes` select l0.id as id,sum(l0.count) as n from ((select `from` as id,count(1) as `count` from `edges` group by `from`) union (select `to` as id,count(1) as `count` from `edges` group by `to`)) as l0 group by l0.id order by l0.id")
				con.commit()
				return

def mysql_trajectory_point_count(con, cur, day, trajectory):
	cur.execute("select count(1) from points where day=%s and trajectory=%s", (day, trajectory,))
	results = cur.fetchall()
	for result in results:
		print(result[0])
	return

def mysql_day_point_count(con, cur, day):
	cur.execute("select count(1) from points where day=%s", (day,))
	results = cur.fetchall()
	for result in results:
		print(result[0])
	return

def mysql_neighbor_count(con, cur, node):
	cur.execute("select n from `nodes` where id=%s", (node,))
	results = cur.fetchall()
	for result in results:
		print(result[0])
	return

def mysql_reachability_count(con, cur, node):
	visited = []
	tovisit = [node]

	while len(tovisit) > 0:
		query = "select `to` from `edges` where `from` in ("
		for i in range(0, len(tovisit)-1):
			query += "%s,"
		query += "%s)"

		visited.extend(tovisit)
		visited = list(set(visited))

		cur.execute(query, tovisit)
		results = cur.fetchall()
		tovisit = []
		for result in results:
			if result[0] not in visited:
				tovisit.append(result[0])

	print(len(visited))


con = pymysql.connect(host="localhost", user="client", database="assignment4")
cur = con.cursor()

#mysql_import_trajectories(con, cur, "Data")
#mysql_import_roadNet(con, cur, "roadNet-CA.txt")

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

average = 0
min = 999999999
max = 0

for i in range(0, 10):
	start = time.clock()
	mysql_neighbor_count(con, cur, i)
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

average = 0
min = 999999999
max = 0

for i in range(0, 10):
	start = time.clock()
	mysql_reachability_count(con, cur, i)
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




