'''
This will extract features and classify the segments
@Author: Rohith Uppala
'''

import pdb
import math

def get_hotel_ratings_dict():
	hotel_ratings_dict = {}
	for line in open("../train/Hotel.csv", "r"):
		try:
			line = line.strip()
			hotel_id, rating = line.split(",")[0], int(line.split(",")[4])
			hotel_ratings_dict[hotel_id] = rating
		except:
			print "I am down"
	return hotel_ratings_dict

def get_hotel_segments_dict():
	hotel_segments_dict = {}
	for line in open("../train/train_search.csv", "r"):
		try:
			hotel_data = line.strip().split(",")
			hotel_id, segment = hotel_data[0], hotel_data[len(hotel_data) - 1]
			hotel_segments_dict[hotel_id] = segment
		except:
			print "i am also wrong here"
	return hotel_segments_dict
	
def process():
	hotel_ratings_dict = get_hotel_ratings_dict()
	hotel_segments_dict = get_hotel_segments_dict()
	classified_dict = {}
	for k, v in hotel_ratings_dict.items():
		rating, segment = v, hotel_segments_dict.get(k, None)
		if not segment: continue
		if rating not in classified_dict:
			classified_dict[rating] = {}
			classified_dict[rating][segment] = 1
		else:
			if segment not in classified_dict[rating]:
				classified_dict[rating][segment] = 1
			else:
				classified_dict[rating][segment] += 1	
	return classified_dict

result = process()
print result
