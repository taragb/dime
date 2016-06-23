#!/usr/bin/python
# -*- coding: latin-1 -*-

# FIXME - drop whitespace, commas

import csv, json, numpy

# Number of personnel fulfilling the organigramme type
#FIXME - agent_services_statistiques not mentioned in xls
def personnel(row):

	personnel = {};

	if(row['ic_a_01-agent_secretaire'] == '1'):
		personnel['agent_secretaire'] = True
	else:
		personnel['agent_secretaire'] = False
	if(row['ic_a_01-agent_etat_civil'] == '1'):
		personnel['agent_etat_civil'] = True
	else:
		personnel['agent_etat_civil'] = False
	if(row['ic_a_01-comptable'] == '1'):
		personnel['comptable'] = True
	else:
		personnel['comptable'] = False
	if(row['ic_a_01-regisseur_recettes'] == '1'):
		personnel['regisseur_recettes'] = True
	else:
		personnel['regisseur_recettes'] = False
	if(row['ic_a_01-agent_materiel_transfere'] == '1'):
		personnel['agent_materiel_transfere'] = True
	else:
		personnel['agent_materiel_transfere'] = False
	if(row['ic_a_01-agent_services_statistiques'] == '1'):
		personnel['agent_services_statistiques'] = True
	else:
		personnel['agent_services_statistiques'] = False
	if(row['ic_a_01-agent_service_techniques'] == '1'):
		personnel['agent_service_techniques'] = True
	else:
		personnel['agent_service_techniques'] = False
	if(row['ic_a_01-agent_affaires_domaniales_foncieres'] == '1'):
		personnel['agent_affaires_domaniales_foncieres'] = True
	else:
		personnel['agent_affaires_domaniales_foncieres'] = False

	return {'personnel' : personnel}

#FIXME: SG missing here but with statistiques added (not on spreadsheet) the total still makes 10
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
	# score = int(row['ic_a_03-ordinary_council_meetings']) * 2.5

	initScore = int(row['ic_a_03-ordinary_council_meetings'])
	if initScore == 0:
		score = 0
	if initScore == 1:
		score = 1
	if initScore == 2:
		score = 3
	if initScore == 3:
		score = 4
	if initScore == 4:
		score = 5
	
	return dict(meetings_held=int(row['ic_a_03-ordinary_council_meetings']), meeting_score=score);

# Average attendance for the meetings held in the year
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
		avg = (int(row['ic_a_04-councilor_attendance_meeting1']) + int(row['ic_a_04-councilor_attendance_meeting2']) + int(row['ic_a_04-councilor_attendance_meeting3']) + int(row['ic_a_04-councilor_attendance_meeting4'])) / int(row['ic_a_03-ordinary_council_meetings'])
		perc = (avg*100)/int(row['ic_a_04-total_councilor'])
		score = 0;
		if(perc >=20 and perc <40):
			score = 0 + ((40 - perc) / 20.0);
		if(perc >=40 and perc <60):
			score = 1 + ((60 - perc) / 20.0);
		if(perc >=60 and perc <80):
			score = 4 + ((80 - perc) / 20.0);
		if(perc >=80 and perc <90):
			score =  6 + ((90 - perc) / 10.0);
		if(perc >=90 and perc <100):
			score = 8 + ((100 - perc) / 10.0);
		if(perc >=100):
			score = 10;

		# if row['commune'] == 'BARSALOGHO':
		# 	print avg, perc, score
	return dict(average_attendance=perc, attendance_score=round(score,1));

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
			score = 1 #+ ((200 - (tax/pop)) / 100.0); 
		if( tax/pop >= 200 ):
			score = 2 #+ ((400 - (tax/pop)) / 200.0);
		if( tax/pop >= 400 ):
			score = 3 #+ ((600 - (tax/pop)) / 200.0);
		if( tax/pop >= 600 ):
			score = 4 #+ ((1000 - (tax/pop)) / 400.0);
		if( tax/pop >= 1000 ):
			score = 5 #+ ((1200 - (tax/pop)) / 200.0);
		if( tax/pop >= 1200 ):
			score = 6 #+ ((1400 - (tax/pop)) / 200.0);
		if( tax/pop >= 1400 ):
			score = 7 #+ ((1800 - (tax/pop)) / 400.0);
		if( tax/pop >= 1800 ):
			score = 8 #+ ((2000 - (tax/pop)) / 200.0);
		if( tax/pop >= 2000 ):
			score = 9 #+ ((2200 - (tax/pop)) / 200.0);
		if( tax/pop >= 2200 ):
			score = 10 #+ ((2400 - (tax/pop)) / 200.0);
		if( tax/pop >= 2400 ):
			score = 11 #+ ((2800 - (tax/pop)) / 400.0);
		if( tax/pop >= 2800 ):
			score = 12 #+ ((3000 - (tax/pop)) / 200.0);
		if( tax/pop >= 3000 ):
			score = 13 #+ ((3500 - (tax/pop)) / 500.0);
		if( tax/pop >= 3500 ):
			score = 14 #+ ((4000 - (tax/pop)) / 500.0);
		if( tax/pop >= 4000 ):
			score = 14 #+ ((4500 - (tax/pop)) / 500.0);
		if( tax/pop >= 4500 ):
			score = 15 #+ ((5000 - (tax/pop)) / 500.0);
		if( tax/pop >= 5000 ):
			score = 16 #+ ((5500 - (tax/pop)) / 500.0);
		if( tax/pop >= 5500 ):
			score = 17 #+ ((6000 - (tax/pop)) / 500.0);
		if( tax/pop >= 6000 ):
			score = 18 #+ ((6500 - (tax/pop)) / 500.0);
		if( tax/pop >= 6500 ):
			score = 19 #+ ((7000 - (tax/pop)) / 500.0);
		if( tax/pop >= 7000 ):
			score = 20 #+ ((7500 - (tax/pop)) / 500.0);
		if( tax/pop >= 7500 ):
			score = 25



		return dict(tax_raised=tax/pop,tax_score=round(score,1));
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
			score = 1 #+ ((65 - perc) / 5.0);
		if(perc >= 65):
			score = 2 #+ ((70 - perc) / 5.0);
		if(perc >= 70):
			score = 3 #+ ((75 - perc) / 5.0);
		if(perc >= 75):
			score = 4 #+ ((80 - perc) / 5.0);
		if(perc >= 80):
			score = 5 #+ ((85 - perc) / 5.0);
		if(perc >= 85):
			score = 6 #+ ((90 - perc) / 5.0);
		if(perc >= 90):
			score = 7 #+ ((95 - perc) / 5.0);
		if(perc >= 95):
			score = 9 #+ ((100 - perc) / 5.0);
		if(perc >= 100):
			score = 10

		return dict(taxes_forecast=perc,taxes_forecast_score=round(score,1));
	except:
		return dict(taxes_forecast=0,taxes_forecast_score=0);


# % completion of their procurement plan
#FIXME: test nonlinear scale junk
def procurement(row):
	score = 0
	proc = float( row['ic_a_07-execution_equipment_procurement_plan'] )

	if(proc >= 20):
		score = 1 #+ ((30 - proc) / 10.0);
	if(proc >= 30):
		score = 2 #+ ((35 - proc) / 5.0);
	if(proc >= 35):
		score = 3 #+ ((40 - proc) / 10.0);
	if(proc >= 40):
		score = 4 #+ ((50 - proc) / 10.0);
	if(proc >= 50):
		score = 5 #+ ((55 - proc) / 5.0);
	if(proc >= 55):
		score = 6 #+ ((60 - proc) / 5.0);
	if(proc >= 60):
		score = 7 #+ ((65 - proc) / 5.0);
	if(proc >= 65):
		score = 8 #+ ((70 - proc) / 5.0);
	if(proc >= 70):
		score = 9 #+ ((75 - proc) / 5.0);
	if(proc >= 75):
		score = 10 #+ ((80 - proc) / 5.0);
	if(proc >= 80):
		score = 11 #+ ((85 - proc) / 5.0);
	if(proc >= 85):
		score = 12 #+ ((90 - proc) / 5.0);
	if(proc >= 90):
		score = 14 #+ ((95 - proc) / 5.0);
	if(proc >= 95):
		score = 16 #+ ((100 - proc) / 5.0);
	if(proc >= 100):
		score = 18

	return dict(procurement=proc,procurement_score=round(score,1));

def demographics(row):
	return dict(commune_type=row['Commune type'],region=row['region'],province=row['province'],commune=row['commune'])

#(REMOVED)calculate how many stars appointed by splitting data into quintiles
# 0 stars = no points at all
# 1 star = bottom quintile among the communes in that category
# 2 star = second to bottom quintile 
# etc. up to five stars
# def get_stars(data, percs):
# 	for d in data:
# 		if(d['total_points'] == 0):
# 			d['stars'] = 0
# 		elif(d['total_points'] > 0 and d['total_points'] < percs[0]):
# 			d['stars'] = 1
# 		elif(d['total_points'] > percs[0] and d['total_points'] < percs[1]):
# 			d['stars'] = 2
# 		elif(d['total_points'] > percs[1] and d['total_points'] < percs[2]):
# 			d['stars'] = 3
# 		elif(d['total_points'] > percs[2] and d['total_points'] < percs[3]):
# 			d['stars'] = 4
# 		elif(d['total_points'] > percs[3] and d['total_points'] < percs[4]):
# 			d['stars'] = 5
# 		else:
# 			d['stars'] = 0

def get_stars(data, percs):
	for d in data:
		d['stars'] = (d['total_points'] / 100) * 5;

rows = []

with open('questionnaire.csv', 'rb') as csvfile:
	infile = csv.DictReader(csvfile, delimiter=',', quotechar='"')
	for row in infile:

		data = dict(personnel(row).items() + demographics(row).items() + number_personnel(row).items() + meetings_held(row).items() + meetings_held2(row).items() + average_attendance(row).items() + tax_raised(row).items() + taxes_forecast(row).items() + procurement(row).items())
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

j = []

for row in rows:
	mm_total = row['number_personnel']
	cm_total = row['meeting_score'] + row['attendance_score'] + row['meeting_score2']
	gf_total = row['tax_score'] + row['taxes_forecast_score'] + row['procurement_score']

	ob = {"label": "COMPÉTENCE MUNICIPALE 2013/14", "year": "2013/14", "commune": row['commune'], "total_points": mm_total + cm_total + gf_total, "max_points": 86, "items":[

				{"label": "MAIRIE/SERVICES MUNICIPAUX", "points": mm_total, "max_points": 10, "personnel": row['personnel']},
				{"label": "CONSEIL MUNICIPAL", "points": cm_total, "max_points": 23, "items": [
					{"label": "Nombre de sessions du Conseil\nMunicipal tenues en 2013", "value": row['meetings_held'], "score": row['meeting_score'], "points": [0,2,5], "scale_marks": [0,2,4]},
					{"label": "Taux de participation aux réunions\nordinaires du Conseil Municipal (%)", "value": row['average_attendance'], "score": row['attendance_score'], "points": [0,1,4,6,8,10], "scale_marks": [20,40,60,80,90,100]},
					{"label": "Nombre de cadre de concertations\norganisés par la mairie en 2013", "value": row['meetings_held2'], "score": row['meeting_score2'], "points": [0,2,4,6,8], "scale_marks": [0,1,2,3,4]}
				]},
				{"label": "GESTION FINANCIERE", "points": gf_total, "max_points": 53, "items": [
					{"label": "Recettes fiscales collectées par\nla commune en 2013, en fonction\nde la population (FCFA/habitant)", "value": row['tax_raised'], "score": row['tax_score'], "points": [0,10,15,25], "scale_marks": [50,2200,4500,7500]},
					{"label": "Taux du recouvrement de taxes en\n2013 en fonction des prévisions (%)", "value": row['taxes_forecast'], "score": row['taxes_forecast_score'], "points": [0,2,4,6,8,10], "scale_marks": [50,60,70,80,90,100]},
					{"label": "Taux d’exécution du plan de\npassation des marchés au\ncours de 2013 (%)", "value": row['procurement'], "score": row['procurement_score'], "points": [0,1,4,7,12,16], "scale_marks": [0,20,40,60,80,100]}
				]}

			]}
	j.append( ob )

totals = []
for item in j:
	totals.append( item['total_points'] )

get_stars(j, numpy.percentile(totals, [20,40,60,80,100]))


with open('tabulated_data.json', 'w') as outfile:
  json.dump(j,outfile, indent=4, separators=(',', ': '))


#write_dict_data_to_csv_file('tabulated_data.csv', rows)
