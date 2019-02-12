import urllib.request, json, math

#the list of building latitudes and longitudes
with open('./data/latlong.json') as f:
	latlong = json.load(f)

#raw_json can either be one time or a whole day
#date is the date the data is from
#scale by overall max tells if weight should be scaled by the highest device count on campus or by the highest count for that building 
def parse_data(raw_json, date):
	data = []
	heatmap = []
	timestamp = []
	max_devices = [0, 0]
	building_max_devices = {}
	#the json is a dictionary of dictionaries of dictionaries of dictionaries of dictionaries. pretty gross
	for date, value in raw_json["Buildings"].items():
		for time, values in value.items():
			#values is the dictionary at a given time of all buildings and their connected devices
			points = []
			timestamp.append(time + ' ' + date)
			for why_so_many_dictionaries, valuess in values.items():
				for building_number, building_data in valuess.items():
					building_name = building_data[0]['buildingName']
					#we only extract the device data if we have the building's lat and long
					if building_name in latlong.keys():
						building_devices = float(building_data[0]['numberOfDevices'])
						if building_name in building_max_devices.keys():
							if building_max_devices[building_name] < building_devices:
								building_max_devices[building_name] = building_devices
						else:
							building_max_devices[building_name] = building_devices
						#this tracks the highest connected building
						if building_devices > max_devices[0]:
							max_devices = [building_devices, building_name]

						# building_prev_devices[building_name] = building_devices
						points.append([building_name, float(latlong[building_name][0]), float(latlong[building_name][1]), building_devices])

			data.append(points)

	return(data, timestamp, max_devices, building_max_devices)

def normalize_data(data, max_devices, building_max_devices, scale_by_overall_max):
	heatmap = []
	for i in range(len(data)):
		points = []
		for j in range(len(data[i])):
			weight = data[i][j][3]
			if weight > 0.0:
				building_name = data[i][j][0]
				latitude = data[i][j][1]
				longitude = data[i][j][2]
				if scale_by_overall_max: 
					weight = math.log(weight + 2, max_devices[0])
				else:
					if building_max_devices[building_name] > 1.0:
						weight = math.log(weight + 2, building_max_devices[building_name])
				points.append([latitude, longitude, weight])
		heatmap.append(points)
	return(heatmap)


def sparse_data(parsed_data, parsed_data2, normalized_data, normalized_data2):
	sparsed_data = []
	sparsed_data2 = []
	sparsed_datai = []
	sparsed_data2i = []
	for i in range(len(normalized_data) - 1):
		if i % 6 == 0:
			sparsed_data.append(normalized_data[i])
			sparsed_data2.append(normalized_data2[i])
			sparsed_datai.append(parsed_data[1][i])
			sparsed_data2i.append(parsed_data2[1][i])

	return([sparsed_data + sparsed_data2, sparsed_datai + sparsed_data2i])

#Gets most recent data formatted correctly for folium heatmap
def get_most_recent(scale_by_overall_max = True):
	url = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/mostrecent'
	request = urllib.request.urlopen(url)
	data = json.load(request)
	data = parse_data(data, date='today')
	return([normalize_data(data[0], data[2], data[3], scale_by_overall_max=scale_by_overall_max)])

# date is day date. scale by overall max is true if you want the weight of points to be scaled by the max 
def get_day_data(date, scale_by_overall_max=True):
	#request 1 because api cant do the whole day at the same time
	url = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/daterange?startdate=' + date + '&enddate=' + date + '&starttime=00:00&endtime=12:00'
	request = urllib.request.urlopen(url)
	data = json.load(request)

	#request 2 because api cant do the whole day at the same time
	url2 = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/daterange?startdate=' + date + '&enddate=' + date + '&starttime=12:00&endtime=24:00'
	request2 = urllib.request.urlopen(url2)
	data2 = json.load(request2)

	parsed_data = parse_data(data, date=date)
	parsed_data2 = parse_data(data2, date=date)

	normalized_data = normalize_data(parsed_data[0], parsed_data[2], parsed_data2[3], scale_by_overall_max=scale_by_overall_max)
	normalized_data2 = normalize_data(parsed_data2[0], parsed_data2[2], parsed_data2[3], scale_by_overall_max=scale_by_overall_max)

	return(sparse_data(parsed_data, parsed_data2, normalized_data, normalized_data2))




