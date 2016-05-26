'''
Convert the data into the model we required and apply a random forest classifier to get
the results we required

@Author: Rohith Uppala
'''

import pdb
import math
import time
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from numpy import genfromtxt, savetxt

class CustomerSegmentation(object):
	def __init__(self):
		self.hotel_star_dict = {}
		self.hotel_user_dict = {}
		self.rf = RandomForestClassifier(n_estimators=100)

	def get_star_rating(self):
		for line in open("../train/Hotel.csv", "r"):
			try:
				hotel_data = line.strip().split(",")
				hotel_id, star_rating = hotel_data[0], int(hotel_data[4])
				self.hotel_star_dict[hotel_id] = star_rating
			except Exception, e:
				print "Error in getting star rating: %s" %(str(e))

	def get_user_rating(self):
		for line in open("../train/Hotel.csv", "r"):
			try:	
				hotel_data = line.strip().split(",")
				hotel_id, user_rating = hotel_data[0], float(hotel_data[5])
				self.hotel_user_dict[hotel_id] = user_rating
			except Exception, e:
				print "Error in getting user rating: %s" %(str(e))
	
	def convert_train_data(self):
		self.get_star_rating()
		self.get_user_rating()
		training_data, prices = [], []		
		for line in open("../train/train_search.csv", "r"):
			try:
				hotel_data = line.strip().split(",")
				hotel_id, age, gender = hotel_data[2], hotel_data[3], hotel_data[4]
				checkin, checkout, room_cnt = hotel_data[6], hotel_data[7], hotel_data[5]
				price, isclicked, isbooked = hotel_data[8], hotel_data[9], hotel_data[10]
				segment = hotel_data[len(hotel_data) - 1]
				gender = 1 if gender == "male" else 0
				isclicked = 1 if isclicked == "true" else 0
				isbooked = 1 if isbooked == "true" else 0
				if segment == "family": segment = 2
				elif segment == "backpacker": segment = 1
				else: segment = 3
				checkin, checkout = datetime.strptime(checkout, "%Y-%m-%d"), datetime.strptime(checkout, "%Y-%m-%d")
				duration = (checkout - checkin).days
				price, room_cnt, age = int(price), int(room_cnt), int(age) / 10
				star_rating = self.hotel_star_dict.get(hotel_id, 0.0)
				user_rating = self.hotel_user_dict.get(hotel_id, 0.0)
				training_data.append([segment, age, price, star_rating, user_rating])			
				prices.append(price)
			except Exception, e:
				print "i am in first line: %s" %(str(e))
		mini, maxi = min(prices), max(prices)
		for i in xrange(len(training_data)):
			old_price = training_data[i][3]
			training_data[i][3] = int((old_price - mini)  * 100.0 / (maxi - mini)) / 10
		return training_data	

	def train_algorithm(self):
		print "Getting transformed data..."
		training_data = self.convert_train_data()
		print "Done!!!"
		target = [x[0] for x in training_data]
		train  = [x[1:] for x in training_data]
		print "Training Random Forest Classifier......"
		self.rf.fit(train, target)
		print "Done"

	def test_algorithm(self):
		print "testing...."
		testing_data, segment_data = [], []
		for line in open("../test/Evaluation.csv", "r"):
			hotel_data = line.strip().split(",")
			hotel_id, age, gender = hotel_data[2], hotel_data[3], hotel_data[4]
			checkin, checkout, room_cnt = hotel_data[6], hotel_data[7], hotel_data[5]
			price, isclicked, isbooked = hotel_data[8], hotel_data[9], hotel_data[10]
			segment = hotel_data[len(hotel_data) - 1]
			gender = 1 if gender == "male" else 0
			isclicked = 1 if isclicked == "TRUE" else 0
			isbooked = 1 if isbooked == "TRUE" else 0
			if segment == "family": segment = 2
			elif segment == "backpacker": segment = 1
			else: segment = 3
			segment_data.append(segment)
#			checkin, checkout = datetime.strptime(checkout, "%Y-%m-%d"), datetime.strptime(checkout, "%Y-%m-%d")
			checkin, checkout = datetime.strptime(checkout, "%d-%m-%Y"), datetime.strptime(checkout, "%d-%m-%Y")
			duration = (checkout - checkin).days
			price, room_cnt, age = int(price), int(room_cnt), int(age) / 10
			star_rating = self.hotel_star_dict.get(hotel_id, 0.0)
			user_rating = self.hotel_user_dict.get(hotel_id, 0.0)
			testing_data.append([age, price, star_rating, user_rating])	
		result_data = self.rf.predict(testing_data)
#		accuracy = f1_score(segment_data, result_data, average='macro')
#		print "Accuracy: ", accuracy
		open("../test/main_result.csv", "w").close()
		ofile = open("../test/main_result.csv", "a")
		index = 0
		for line in open("../test/Evaluation.csv", "r"):
			search_id = line.strip().split(",")[0]
			result = result_data[index]
			ofile.write(search_id + "," + str(result) + "\n")
			index = index + 1
		ofile.close()

if __name__ == "__main__":
	cf = CustomerSegmentation()
	cf.train_algorithm()
	cf.test_algorithm()
