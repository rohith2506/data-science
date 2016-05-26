from datetime import datetime, timedelta

def get_duration_dict():
	duration_dict = {}
	for line in open("../train/train_search.csv", "r"):
		try:
			hotel_data = line.strip().split(",")
			checkin, checkout, segment = hotel_data[6], hotel_data[7], hotel_data[len(hotel_data) - 1]
			checkin = datetime.strptime(checkin, "%Y-%m-%d")
			checkout = datetime.strptime(checkout, "%Y-%m-%d")
			diff_days = (checkout - checkin).days
			if diff_days not in duration_dict:
				duration_dict[diff_days] = {}
				duration_dict[diff_days][segment] = 1
			else:
				if segment not in duration_dict[diff_days]:
					duration_dict[diff_days][segment] = 1
				else:
					duration_dict[diff_days][segment] += 1
		except:
			print "i am the first line"
	return duration_dict

def get_reverse_duration_dict():
	duration_dict = {}
	for line in open("../train/train_search.csv", "r"):
		try:
			hotel_data = line.strip().split(",")
			checkin, checkout, segment = hotel_data[6], hotel_data[7], hotel_data[len(hotel_data) - 1]
			checkin = datetime.strptime(checkin, "%Y-%m-%d")
			checkout = datetime.strptime(checkout, "%Y-%m-%d")
			diff_days = (checkout - checkin).days
			if segment not in duration_dict:
				duration_dict[segment] = {}
				duration_dict[segment][diff_days] = 1
			else:
				if diff_days not in duration_dict[segment]:
					duration_dict[segment][diff_days] = 1
				else:
					duration_dict[segment][diff_days] += 1
		except:
			print "i am the first line"
	return duration_dict

print get_duration_dict()
print get_reverse_duration_dict()
