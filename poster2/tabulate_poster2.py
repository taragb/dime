#!/usr/bin/python
# -*- coding: latin-1 -*-

import csv, json, os, time
import pandas as pd
import numpy as np
import math


alldata = pd.read_csv("data_files/aggregate_final.csv")

full = alldata


def projected_births(row):
	score = 0; 
	calc = float(row['projected_births'])

	if(calc >= .2):
		score = 1;
	if(calc >= .3):
		score = 2;
	if(calc >= .4):
		score = 3;
	if(calc >= .5):
		score = 4;
	if(calc >= .6):
		score = 5;
	if(calc >= .7):
		score = 6;
	if(calc >= .8):
		score = 7;
	if(calc >= .85):
		score = 8;
	if(calc >= .9):
		score = 9;
	if(calc >= .95):
		score = 10;
	if(calc >= 1):
		score = 12;

	# if row['COMMUNE'] == 'ABSOUYA':
	# 	print calc, score

	return score;

full['s_projected_births'] = full.apply(projected_births, axis=1)


def passing_exam(row):
	national_average = 65.2;
	national_pct = .652
	score = 0
	calc = (float(row['passing_exam']) - national_pct)

	if(calc <= -.4):
		score = 0
	elif(calc <= -.35):
		score = 1
	elif(calc <= -.30):
		score = 2
	elif(calc <= -.25):
		score = 3
	elif(calc <= -.2):
		score = 4
	elif(calc <= -.15):
		score = 5
	elif(calc <= -.1):
		score = 6
	elif(calc <= -.05):
		score = 7
	elif(calc <= .05):
		score = 8
	elif(calc <= .1):
		score = 9
	elif(calc <= .15):
		score = 10
	elif(calc <= .2):
		score = 12
	elif(calc <= .25):
		score = 14
	elif(calc <= .35):
		score = 18
	elif(calc > .35):
		score = 20

	# if row['COMMUNE'] == 'ABSOUYA':
	# 	print calc, row['passing_exam'], score

	return score

full['s_passing_exam'] = full.apply(passing_exam, axis=1)

def passing_exam_val(row):
	national_average = 65.2;
	national_pct = .652
	score = 0
	calc = (float(row['passing_exam']) - national_pct)
	calc = int(round(calc*100))
	return calc

full['passing_exam_val'] = full.apply(passing_exam_val, axis=1)


def functional_water_score(row):
	score = 0
	calc = float(row['functional_water'])/100

	if(calc <= .1):
		score = 0
	elif(calc < .2):
		score = 1
	elif(calc < .25):
		score = 2
	elif(calc < .3):
		score = 3
	elif(calc < .35):
		score = 4
	elif(calc < .4):
		score = 5
	elif(calc < .45):
		score = 6
	elif(calc < .5):
		score = 7
	elif(calc < .55):
		score = 8
	elif(calc < .6):
		score = 9
	elif(calc < .65):
		score = 10
	elif(calc < .7):
		score = 11
	elif(calc < .75):
		score = 12
	elif(calc < .8):
		score = 13
	elif(calc < .85):
		score = 14
	elif(calc < .9):
		score = 15
	elif(calc < .95):
		score = 16
	elif(calc < 1):
		score = 20
	elif(calc >= 1):
		score = 25

	# if row['COMMUNE'] == 'ABSOUYA':
	# 	print calc, score

	return score

full['s_functional_water'] = full.apply(functional_water_score, axis=1)



def latrines_score(row):
	score = 0
	calc = row['latrines_per_class']

	if(calc <= .25):
		score = 0
	if(calc >= .3):
		score = 1
	if(calc >= .35):
		score = 2
	if(calc >= .4):
		score = 3
	if(calc >= .50):
		score = 4
	if(calc >= .55):
		score = 5
	if(calc >= .6):
		score = 6
	if(calc >= .65):
		score = 7
	if(calc >= .70):
		score = 8
	if(calc >= .75):
		score = 9
	if(calc >= .8):
		score = 10
	if(calc >= .85):
		score = 11
	if(calc >= .9):
		score = 12
	if(calc >= .95):
		score = 14
	if(calc >= 1):
		score = 15
	
	# if row['COMMUNE'] == 'SINDOU':
	# 	print calc, score

	return score

full['s_latrines'] = full.apply(latrines_score, axis=1)


def supplies_score(row):
	score = 0
	# calc = round(row['supplies_received'])
	calc = row['supplies_received']

	score = max(0,10 - math.sqrt(3*calc))

	# if row['COMMUNE'] == 'ABSOUYA':
		# print round(calc), math.floor(score)

	return math.floor(score)

full['s_supplies'] = full.apply(supplies_score, axis=1)

def csps_score(row):
	score = 0
	calc = row['csps_val']
	score = float(calc)*10

	# if row['COMMUNE'] == 'ABSOUYA':
		# print calc, score

	return round(score)

full['s_csps'] = full.apply(csps_score, axis=1)

def assisted_birth_score(row):
	score = 0
	calc = row['assisted_births']

	if(calc <= .35):
		score = 0
	if(calc >= .4):
		score = 1
	if(calc >= .55):
		score = 2
	if(calc >= .6):
		score = 4
	if(calc >= .65):
		score = 5
	if(calc >= .7):
		score = 7
	if(calc >= .75):
		score = 8
	if(calc >= .8):
		score = 9
	if(calc >= .85):
		score = 10
	if(calc >= .9):
		score = 11
	if(calc >= .95):
		score = 12
	if(calc >= 1):
		score = 13
	if(calc >= 1.1):
		score = 14
	if(calc >= 1.2):
		score = 15

	# if row['COMMUNE'] == 'SINDOU':
	# 	print calc, score

	return score

full['s_assisted_births'] = full.apply(assisted_birth_score, axis=1)

def vaccine_score(row):
	score = 0
	calc = row['vac_total']

	if(calc <= .55):
		score = 0
	if(calc >= .6):
		score = 1
	if(calc >= .65):
		score = 2
	if(calc >= .7):
		score = 3
	if(calc >= .75):
		score = 5
	if(calc >= .8):
		score = 7
	if(calc >= .85):
		score = 8
	if(calc >= .9):
		score = 9
	if(calc >= 1):
		score = 10
	if(calc >= 1.2):
		score = 12
	if(calc >= 1.4):
		score = 14
	if(calc >= 1.5):
		score = 15

	# if row['COMMUNE'] == 'TIKARE':
	# 	print calc, score

	return score

full['s_vaccine'] = full.apply(vaccine_score, axis=1)

def water_score(row):
	score = 0
	calc = row['water_access']

	if(calc <= .15):
		score = 0
	if(calc >= .2):
		score = 1
	if(calc >= .25):
		score = 2
	if(calc >= .3):
		score = 3
	if(calc >= .35):
		score = 4
	if(calc >= .4):
		score = 5
	if(calc >= .45):
		score = 6
	if(calc >= .5):
		score = 7
	if(calc >= .55):
		score = 8
	if(calc >= .60):
		score = 9
	if(calc >= .65):
		score = 10
	if(calc >= .70):
		score = 11
	if(calc >= .75):
		score = 12
	if(calc >= .8):
		score = 13
	if(calc >= .85):
		score = 14
	if(calc >= .9):
		score = 16
	if(calc >= .95):
		score = 18

	# if row['COMMUNE'] == 'ABSOUYA':
	# 	print calc, score

	return score

full['s_water_access'] = full.apply(water_score, axis=1)

#full = full.reindex(columns=['COMMUNE', 's_vaccine','s_supplies','s_water_access','s_passing_exam','s_assisted_births','s_latrines','s_projected_births'])

tabulated = full.to_dict(outtype='records')

def get_stars(data, percs):
	for d in data:
		d['stars'] = int( (d['total_points'] / 140.0) / .2);

j = []

for row in tabulated:

	#set score to 0 if the value doesn't exist
	fw = row['s_functional_water']
	if (fw == None):
		fw = 0.0
	csps = row['s_csps']
	if math.isnan(csps):
		csps = 0.0

	ecoles_total = row['s_passing_exam'] + row['s_supplies'] + row['s_latrines'] + fw
	sante_total = row['s_assisted_births'] + row['s_vaccine'] + csps

	total_total = ecoles_total + sante_total + row['s_water_access'] + row['s_projected_births']

	ob = {"label": "COMPÉTENCE MUNICIPALE 2013/14", "year": "2013/14", "commune": row['COMMUNE'], "total_points": total_total, "max_points": 140, "items":[

			{"label": "ÉCOLES PRIMAIRES", "points": ecoles_total, "max_points": 70, "items": [
				{"label": "Écart entre le taux d'admission du\nCEP dans la commune et au niveau\nnational (en points de pourcentage)", "value": row['passing_exam_val'], "score": row['s_passing_exam'], "points": [0,4,8,14,18], "scale_marks": [-40,-20,0,20,35]},
				{"label": "Retard moyen d'approvisionnement en\n fournitures scolaires (mesuré en nombre de\njours après la rentrée scolaire)", "value": round(row['supplies_received']), "score": row['s_supplies'], "points": [0,1,3,6,10], "scale_marks": [30,25,15,4,0]}, #FIX - TARA
				{"label": "Taux d'écoles avec un forage fonctionnel", "value": row['functional_water'], "score": row['s_functional_water'], "points": [0,2,8,12,25], "scale_marks": [0,25,50,75,100]},
				{"label": "Taux d’écoles avec des latrines\nfonctionnelles pour chaque classe", "value": row['latrines_per_class'] * 100, "score": row['s_latrines'], "points": [0,3,6,10,15], "scale_marks": [25,40,60,80,100]}
			]},
			{"label": "SANTÉ", "points": sante_total, "max_points": 40, "items": [
				{"label": "Taux d’accouchements assistés\npendant l’année", "value": row['assisted_births'] * 100, "score": row['s_assisted_births'], "points": [0,5,10,15], "scale_marks": [35,65,85,100]},
				{"label": "Taux de nourrissons 0-11 mois ayant été\nvaccinés avec le BCG, VAR, VAA, VPO3,\nDTC-Hep+Hib3 en 2013", "value": row['vac_total'] * 100, "score": row['s_vaccine'], "points": [0,3,5,7,15], "scale_marks": [55,65,75,90,100]},
				{"label": "Taux de CSPS ayant reçu un stock de Gaz de la\nmunicipalité entre juin et décembre 2013", "value": row['csps_val']*100, "score": row['s_csps'], "points": [0,5,8,10], "scale_marks": [0,50,80,100]}  
			]},
			{"label": "EAU ET ASSAINISSEMENT", "points": row['s_water_access'], "max_points": 18, "items": [
				{"label": "Taux de la population avec accès à\nune source d’eau potable fonctionnelle à\n1000m pour 300 personnes/forage", "value": row['water_access']*100, "score": row['s_water_access'], "points": [0,4,8,12,18], "scale_marks": [15,35,55,75,100]}
			]},
			{"label": "ACTES DE NAISSANCES", "points": row['s_projected_births'], "max_points": 12, "items": [
				{"label": "Taux d’actes de naissances\ndélivrés comparé aux naissances\nattendues", "value": row['projected_births'] * 100, "score": row['s_projected_births'], "points": [0,1,3,5,7,12], "scale_marks": [10,20,45,60,80,100]}
			]}

		]}

	j.append(ob);

totals = []
for item in j:
	totals.append( item['total_points'] )

get_stars(j, np.percentile(totals, [20,40,60,80,100]))



with open('poster2_data.json', 'w') as outfile:
  json.dump(j,outfile, indent=4, separators=(',', ': '))

