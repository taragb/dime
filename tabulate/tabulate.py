# FIXME - drop whitespace, commas

import csv

# Number of personnel fulfilling the organigramme type
#FIXME - agent_services_statistiques not mentioned in xls
def number_personnel(row):
	score = 0;
	if(row['ic_a_01-agent_secretaire'] == '1'):
		score += 1;
	if(row['ic_a_01-agent_etat_civil'] == '1'):
		score += 2;
	if(row['ic_a_01-comptable'] == '1'):
		score += 2;
	if(row['ic_a_01-regisseur_recettes'] == '1'):
		score += 1;
	if(row['ic_a_01-agent_materiel_transfere'] == '1'):
		score += 1;
	if(row['ic_a_01-agent_services_statistiques'] == '1'):
		score += 1;
	if(row['ic_a_01-agent_service_techniques'] == '1'):
		score += 1;
	if(row['ic_a_01-agent_affaires_domaniales_foncieres'] == '1'):
		score += 1;

	return dict(number_personnel=score);

# Number of Meetings Held (1-4)
def meetings_held(row):
	score = int(row['ic_a_03-ordinary_council_meetings'])
	if(score >= 2):
		score += 1;
	if(score > 5):
		score = 5;
	return dict(meetings_held=int(row['ic_a_03-ordinary_council_meetings']), meeting_score=score);

# Average attendance for the meetings held in the year
# FIXME - do I take the average of meetings attended or the overall average
def average_attendance(row):
	if( row['ic_a_04-councilor_attendance_meeting1'] == ''):
		row['ic_a_04-councilor_attendance_meeting1'] = 0;
	if( row['ic_a_04-councilor_attendance_meeting2'] == ''):
		row['ic_a_04-councilor_attendance_meeting2'] = 0;
	if( row['ic_a_04-councilor_attendance_meeting3'] == ''):
		row['ic_a_04-councilor_attendance_meeting3'] = 0;
	if( row['ic_a_04-councilor_attendance_meeting4'] == ''):
		row['ic_a_04-councilor_attendance_meeting4'] = 0;

	if(int(row['ic_a_03-ordinary_council_meetings']) == 0 ):
		score = 0
		perc = 0
	else:
		perc = int(row['ic_a_04-councilor_attendance_meeting1']) + int(row['ic_a_04-councilor_attendance_meeting2']) + int(row['ic_a_04-councilor_attendance_meeting3']) + int(row['ic_a_04-councilor_attendance_meeting4']) / int(row['ic_a_03-ordinary_council_meetings'])
		score = 0;
		if(perc >=40):
			score = 1;
		if(perc >=60):
			score = 4;
		if(perc >=80):
			score = 6;
		if(perc >=90):
			score = 8;
		if(perc >=100):
			score = 10;
	return dict(average_attendance=perc, attendance_score=score);

# Number of meetings Held (0-4): How many of these meetings were held: ic_a_05-CdC_meetings_2013
def meetings_held2(row):
	meetings = int( row['ic_a_05-CdC_meetings_2013'] )
	score = meetings * 2

	return dict(meetings_held2=meetings, meeting_score2=score);

# Local Taxes Raised 2013/ Population of Commune
def tax_raised(row):
	try:
		tax = int(row['ic_a_06-local_taxes_2012'])
		pop = int(row['commune_population_number'])

		score = 0

		if( tax/pop >= 100 ):
			score = 1
		if( tax/pop >= 200 ):
			score = 2
		if( tax/pop >= 400 ):
			score = 3
		if( tax/pop >= 600 ):
			score = 4
		if( tax/pop >= 1000 ):
			score = 5
		if( tax/pop >= 1200 ):
			score = 6
		if( tax/pop >= 1400 ):
			score = 7
		if( tax/pop >= 1800 ):
			score = 8
		if( tax/pop >= 2000 ):
			score = 9
		if( tax/pop >= 2200 ):
			score = 10
		if( tax/pop >= 2400 ):
			score = 11
		if( tax/pop >= 2800 ):
			score = 12
		if( tax/pop >= 3000 ):
			score = 13
		if( tax/pop >= 3500 ):
			score = 14
		if( tax/pop >= 4000 ):
			score = 14
		if( tax/pop >= 4500 ):
			score = 15
		if( tax/pop >= 5000 ):
			score = 16
		if( tax/pop >= 5500 ):
			score = 17
		if( tax/pop >= 6000 ):
			score = 18
		if( tax/pop >= 6500 ):
			score = 19
		if( tax/pop >= 7000 ):
			score = 20
		if( tax/pop >= 7500 ):
			score = 25



		return dict(tax_raised=tax/pop,tax_score=score);
	except:
		return dict(tax_raised=0,tax_score=0);
	
# Local Taxes Raised 2013/ Forecast for 2013
def taxes_forecast(row):
	score = 0
	try:
		actual = float(row['ic_a_06-local_taxes_2012'].strip())
		forecast = float(row['ic_a_06-local_taxes_forecast_2012'].strip())

		perc = round((actual/forecast) * 100, 2)

		if(perc >= 60):
			score = 1
		if(perc >= 65):
			score = 2
		if(perc >= 70):
			score = 3
		if(perc >= 75):
			score = 4
		if(perc >= 80):
			score = 5
		if(perc >= 85):
			score = 6
		if(perc >= 90):
			score = 7
		if(perc >= 95):
			score = 9
		if(perc >= 100):
			score = 10

		return dict(taxes_forecast=perc,taxes_forecast_score=score);
	except:
		return dict(taxes_forecast=0,taxes_forecast_score=0);


# % completion of their procurement plan
def procurement(row):
	score = 0
	proc = float( row['ic_a_07-execution_equipment_procurement_plan'] )

	if(proc >= 20):
		score = 1
	if(proc >= 30):
		score = 2
	if(proc >= 35):
		score = 3
	if(proc >= 40):
		score = 4
	if(proc >= 50):
		score = 5
	if(proc >= 55):
		score = 6
	if(proc >= 60):
		score = 7
	if(proc >= 65):
		score = 8
	if(proc >= 70):
		score = 9
	if(proc >= 75):
		score = 10
	if(proc >= 80):
		score = 11
	if(proc >= 85):
		score = 12
	if(proc >= 90):
		score = 14
	if(proc >= 95):
		score = 16
	if(proc >= 100):
		score = 18

	return dict(procurement=proc,procurement_score=score);

def demographics(row):
	return dict(commune_type=row['Commune type'],region=row['region'],province=row['province'],commune=row['commune'])

rows = []

with open('questionnaire.csv', 'rb') as csvfile:
	infile = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	for row in infile:

		data = dict(demographics(row).items() + number_personnel(row).items() + meetings_held(row).items() + meetings_held2(row).items() + average_attendance(row).items() + tax_raised(row).items() + taxes_forecast(row).items() + procurement(row).items())
		rows.append(data)

def write_dict_data_to_csv_file(csv_file_path, dict_data):
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = dict_data[0].keys()
    writer.writerow(headers)

    for dat in dict_data:
        line = []
        for field in headers:
            line.append(dat[field])
        writer.writerow(line)
        
    csv_file.close()

write_dict_data_to_csv_file('tabulated_data.csv', rows)
