impory MySQLdb

db = MySQLdb.connect(host="localhost", user="client", database="assignment4")
cur = db.cursor()

def mysql_import(store, directory):
	t = 0
	for trajectory in os.listdir(directory):
		p = 0
		for plt in os.listdir(directory + "/" + trajectory + "/Trajectory"):
			with open(directory + "/" + trajectory + "/Trajectory/" + plt) as trace:
				l = -1
				for line in csv.reader(trace):
					if l != -1:
						
						l += 1
					elif len(line) == 1 and line[0] == "0":
						l = 0
			
			print("trajectory:" + str(t) + ":" + str(p))
			p += 1
		#print("trajectory:" + str(t))
		t += 1
	return



