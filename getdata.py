import urllib.request, json, math

with open('./data/latlong.json') as f:
	latlong = json.load(f)

def parse_data(raw_json, animated, date):
	heatmap = []
	timestamp = []
	for date, value in raw_json["Buildings"].items():
		for time, values in value.items():
			buildings  = []
			points     = []
			latitudes  = []
			longitudes = []
			devices    = []
			timestamp.append(time + ' ' + date)

			for why_so_many_dictionaries, valuess in values.items():
				for building_number, building_data in valuess.items():
					building = building_data[0]['buildingName']
					if building in latlong.keys():
						buildings.append(building)
						latitudes.append(float(latlong[building][0]))
						longitudes.append(float(latlong[building][1]))
						devices.append(float(building_data[0]['numberOfDevices']))

			maximum_devices = max(devices)
			for i in range(len(devices)):
				if devices[i] > 0:
					devices[i] = math.log(devices[i], maximum_devices) + .1
				points.append([latitudes[i], longitudes[i], devices[i]])

			heatmap.append(points)


	return(heatmap, timestamp)

#Gets most recent data formatted correctly for folium heatmap
def get_most_recent():
	url = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/mostrecent'
	request = urllib.request.urlopen(url)
	data = json.load(request)
	return(parse_data(data, animated=False, date='today'))

def get_day_data(date):
	#request 1 because api cant do the whole day at the same time
	url = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/daterange?startdate=' + date + '&enddate=' + date + '&starttime=00:00&endtime=12:00'
	request = urllib.request.urlopen(url)
	data = json.load(request)

	#request 2 because api cant do the whole day at the same time
	url2 = 'https://f4wy2zmcz6.execute-api.us-east-1.amazonaws.com/wirelessAPI/daterange?startdate=' + date + '&enddate=' + date + '&starttime=12:00&endtime=24:00'
	request2 = urllib.request.urlopen(url2)
	data2 = json.load(request2)

	parsed_data = parse_data(data, animated=True, date=date)
	parsed_data2 = parse_data(data2, animated=True, date=date)

	sparsed_data = []
	sparsed_data2 = []
	sparsed_datai = []
	sparsed_data2i = []
	for i in range(len(parsed_data[0]) - 1):
		if i % 6 == 0:
			sparsed_data.append(parsed_data[0][i])
			sparsed_data2.append(parsed_data2[0][i])
			sparsed_datai.append(parsed_data[1][i])
			sparsed_data2i.append(parsed_data2[1][i])

	return([sparsed_data + sparsed_data2, sparsed_datai + sparsed_data2i])
