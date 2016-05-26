def get_price():
	price_dict, mini, maxi = {}, 100000000, 0
	for line in open("../train/train_search.csv", "r"):
		try:
			hotel_data = line.strip().split(",")
			price = int(hotel_data[8])
			mini = min(price, mini)
			maxi = max(price, maxi)
		except:
			print "I am the first line"
	return mini, maxi

print get_price()
