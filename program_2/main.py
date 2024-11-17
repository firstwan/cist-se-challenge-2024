import json
import time
from heapq import heappop, heappush, heappushpop
from restaurant import Restaurant, RestaurantEncoder

def main():
	file="./validated_dataset.json"
	# # record start time
	# start = time.time()
	
	with open(file, "r") as file:
		dataset = json.load(file)

	number_of_extract = 10
	print("[#] Sorting the dataset from high to low...")
	heap = []
	for data in dataset:
		if len(heap) < number_of_extract:
			heappush(heap, Restaurant(data))
		else:
			heappushpop(heap, Restaurant(data))

	print(f"[#] Select top {number_of_extract} restaurant...")

	# Pop out the heap with ASC order, then reverse the order
	top_10_restaurant = [None] * number_of_extract
	for index in range(number_of_extract):
		top_10_restaurant[index] = heappop(heap)
	top_10_restaurant = top_10_restaurant[::-1]

	# Serializing json
	print("[#] Creating Json file...")
	json_object = json.dumps(top_10_restaurant, indent=4, cls=RestaurantEncoder)

	# Write data into json file
	with open("topk_results.json", "w+") as outfile:
		outfile.write(json_object)
	print("[#] Json file created.")

	# # record end time
	# end = time.time()
	# print("The time of new json creation :", (end-start) * 10**3, "ms")


main()
