def get_age():
	age_dict = {}
	for line in open("../train/train_search.csv", "r"):
		try:
			line = line.strip()
			hotel_data = line.split(",")
			age, gender, segment = hotel_data[3], hotel_data[4], hotel_data[len(hotel_data) - 1]
			age = int(age) /10
			if age not in age_dict:
				age_dict[age] = {}
				age_dict[age][segment] = 1
			else:
				if segment not in age_dict[age]:
					age_dict[age][segment] = 1
				else:
					age_dict[age][segment] += 1
		except:
			print "I am the first line"
	return age_dict


def get_gender():
	gender_dict = {}
	for line in open("../train/train_search.csv", "r"):
		try:
			line = line.strip()
			hotel_data = line.split(",")
			age, gender, segment = hotel_data[3], hotel_data[4], hotel_data[len(hotel_data) - 1]
			age = int(age) /10
			if gender not in gender_dict:
				gender_dict[gender] = {}
				gender_dict[gender][segment] = 1
			else:
				if segment not in gender_dict[gender]:
					gender_dict[gender][segment] = 1
				else:
					gender_dict[gender][segment] += 1
		except:
			print "I am the first line"
	return gender_dict


print get_gender()				
