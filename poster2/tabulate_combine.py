#!/usr/bin/python
# -*- coding: latin-1 -*-

import csv, json, os, time
import pandas as pd
import numpy as np

ecole = pd.read_csv("data_files/Directeur_ecole_modifie_consolidated.csv");
sanitaire = pd.read_csv("data_files/District_sanitaire_modifie_consolidated_v2.csv");

ceb = pd.read_csv("data_files/CEB_modifie_consolidated.csv");
water_access = pd.read_csv("data_files/water_access.csv");
muni = pd.read_csv("data_files/questionnaire.csv");

# schools with a latrine for each class/ total schools 

def latrines_per_class(row):
	lat_rate = row['sd_a_02-functional_latrines'] / row['number_classes']
	if(lat_rate >= 1.0):
		return 1
	else:
		return 0

ecole['latrines_per_class'] = ecole.apply(latrines_per_class , axis=1)

ecole_group = ecole.groupby('commune')['latrines_per_class'].agg(['sum', 'count'])
lpc = ecole_group['sum'] / ecole_group['count']

# schools with a functional water point/ total schools surveyed (OVER 9 MONTHS)

def functional_water(row):
	if(row['sd_a_01-water_source_functional'] >= 9):
		return 1
	else:
		return 0

ecole['functional_water'] = ecole.apply(functional_water, axis=1)

ecole_group = ecole.groupby('commune')['functional_water'].agg(['sum', 'count'])
fw = ecole_group['sum'] / ecole_group['count']

#supplies recieved Weeks before or after start of school year 

def supplies_recieved(row):
	#print row['sd_a_03-year_month_received_school_supplies']
	t = time.strptime(row['sd_a_03-year_month_received_school_supplies'], "%d-%b-%y")
	week_month = int(time.strftime("%m",t)) - 10
	if(week_month >= 0):
		return (week_month * 4) + int(row['sd_a_03-week_received_school_supplies']) - 1
	else:
		return 0

ecole['supplies_recieved'] = ecole.apply(supplies_recieved, axis=1)
ecole_group = ecole.groupby('commune')['supplies_recieved'].agg(['sum', 'count'])
supp = ecole_group['sum'] / ecole_group['count']

ecole_combined = pd.concat([fw, lpc, supp], axis=1)

ecole_combined.columns = ['functional_water', 'latrines_per_class', 'supplies_recieved']
ecole_combined['commune'] = ecole_combined.index


ceb['passing_exam'] = ceb['sd_a_01-students_admitted_exam'] / ceb['sd_a_01-total_students_sitting_exam'];


sanitaire['assisted_births'] = sanitaire['sd_a_01-assisted_deliveries_1'] /  sanitaire['sd_a_01-projected_deliveries_1']


sanitaire['bcg'] = sanitaire['sd_a_02-vaccination_coverage_BCG_1'] /  sanitaire['sd_a_02-target_vaccination_BCG_1']

sanitaire['vpo3'] = sanitaire['sd_a_03-target_vaccination_VPO3_1'] /  sanitaire['sd_a_03-vaccination_coverage_VPO3_1']

sanitaire['dtc'] = sanitaire['sd_a_04-vaccination_coverage_DTCHepHib3_1'] /  sanitaire['sd_a_04-target_vaccination_DTCHepHib3_1']

sanitaire['var'] = sanitaire['sd_a_05-vaccination_coverage_VAR_1'] /  sanitaire['sd_a_05-target_vaccination_VAR_1']

sanitaire['vaa'] = sanitaire['sd_a_06-vaccination_coverage_VAA_1'] /  sanitaire['sd_a_06-target_vaccination_VAA_1']

sanitaire['vac_total'] = sanitaire['bcg'] * sanitaire['vpo3'] * sanitaire['dtc'] * sanitaire['var'] * sanitaire['vaa']


#print sanitaire['sd_a_01-stock_gas'] 

#print water_access['access']


water_access = water_access.reindex(columns=['COMMUNE', 'access'])

ceb = ceb.reindex(columns=['commune', 'passing_exam'])

#print muni['sd_a_01-birth_certificates']
muni = muni.reindex(columns=['commune', 'sd_a_01-birth_certificates'])
sanitaire = sanitaire.reindex(columns=['commune', 'sd_a_01-projected_deliveries_1', 'vac_total', 'assisted_births'])

full = pd.merge(water_access,ceb,left_on='COMMUNE',right_on='commune')

full = pd.merge(full, muni, left_on='COMMUNE', right_on='commune')

full = pd.merge(full, sanitaire, left_on='COMMUNE', right_on='commune')

full = pd.merge(full, ecole_combined, left_on='COMMUNE', right_on='commune')


def projected_births_value(row):
	return float(row['sd_a_01-birth_certificates']) / float(row['sd_a_01-projected_deliveries_1']);

full['projected_births_v'] = full.apply(projected_births_value, axis=1)


def projected_births(row):
	score = 0; 
	calc = float(row['sd_a_01-birth_certificates']) / float(row['sd_a_01-projected_deliveries_1']);

	if(calc >= .2):
		score = 1;
	if(calc >= .3):
		score += 2;
	if(calc >= .4):
		score = 3;
	if(calc >= .5):
		score = 4;
	if(calc >= .6):
		score += 5;
	if(calc >= .7):
		score += 6;
	if(calc >= .8):
		score += 7;
	if(calc >= .85):
		score += 8;
	if(calc >= .9):
		score += 9;
	if(calc >= .95):
		score += 10;
	if(calc >= 1):
		score += 12;

	return score;

full['s_projected_births'] = full.apply(projected_births, axis=1)


def passing_exam(row):
	national_average = 65.2;
	score = 0
	calc = (float(row['passing_exam']) / national_average) - 1

	if(calc <= -.4):
		score = 0
	if(calc <= -.35):
		score = 1
	if(calc <= -.30):
		score = 2
	if(calc <= -.25):
		score = 3
	if(calc <= -.2):
		score = 4
	if(calc <= -.15):
		score = 5
	if(calc <= -.1):
		score = 6
	if(calc <= -.05):
		score = 7
	if(calc > -0.05):
		score = 8
	if(calc >= .05):
		score = 9
	if(calc >= .1):
		score = 10
	if(calc >= .15):
		score = 12
	if(calc >= .2):
		score = 14
	if(calc >= .25):
		score = 18
	if(calc >= .35):
		score = 20

	return score

full['s_passing_exam'] = full.apply(passing_exam, axis=1)


#fixme need new scale values
def functional_water_score(row):
	score = 0



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
	return score

full['s_latrines'] = full.apply(latrines_score, axis=1)


#fixme I think this is wrong
def supplies_score(row):
	score = 0
	calc = int(row['supplies_recieved'])

	if(calc <= -2):
		score = 10
	if(calc <= 1):
		score = 8
	if(calc == 0):
		score = 5
	if(calc >= 1):
		score = 3
	if(calc >= 2):
		score = 2
	if(calc >= 4):
		score = 1

	return score

full['s_supplies'] = full.apply(supplies_score, axis=1)

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

	return score

full['s_vaccine'] = full.apply(vaccine_score, axis=1)

def water_score(row):
	score = 0
	calc = row['access'] /100.0

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

	return score


full['s_water_access'] = full.apply(water_score, axis=1)

#full = full.reindex(columns=['COMMUNE', 's_vaccine','s_supplies','s_water_access','s_passing_exam','s_assisted_births','s_latrines','s_projected_births'])

tabulated = full.to_dict(outtype='records')

def get_stars(data, percs):
	for d in data:
		d['stars'] = (int(d['total_points']) / 100.0) * 5;

j = []

for row in tabulated:

	#fixme- add water to ecoles total; add missing to sante
	ecoles_total = row['s_passing_exam'] + row['s_supplies'] + row['s_latrines']
	sante_total = row['s_assisted_births'] + row['s_vaccine']

	total_total = ecoles_total + sante_total + row['s_water_access'] + row['s_projected_births']

	ob = {"label": "COMPÉTENCE MUNICIPALE 2013/14", "year": "2013/14", "commune": row['COMMUNE'], "total_points": total_total, "max_points": 110, "items":[

			{"label": "ÉCOLES PRIMAIRES", "points": ecoles_total, "max_points": 40, "items": [
				{"label": "Taux d'Admission du CEP comparé à\nla moyenne nationale", "value": row['passing_exam'] * 100, "score": row['s_passing_exam'], "points": [0,4,8,14,20], "scale_marks": [-40,-20,0,20,35]},
				{"label": "d'écoles recevant les fournitures\nscolaires avant le début de l'année\nscolaire 2013/2014", "value": row['supplies_recieved'] * 100, "score": row['s_supplies'], "points": [0,1,4,6,8,10], "scale_marks": [20,40,60,80,90,100]},
				{"label": "d'écoles avec un forage fonctionnel", "value": row['access'] * 100, "score": row['s_water_access'], "points": [0,2,6,10,14,25], "scale_marks": [10,20,40,60,80,90,100]},
				{"label": "d’écoles avec des latrines\nfonctionnelles pour chaque classe", "value": row['latrines_per_class'] * 100, "score": row['s_latrines'], "points": [0,3,6,10,15], "scale_marks": [25,40,60,80,100]}
			]},
			{"label": "SANTÉ", "points": sante_total, "max_points": 40, "items": [
				{"label": "d’accouchements assistés\npendant l’année", "value": row['assisted_births'] * 100, "score": row['s_assisted_births'], "points": [0,4,8,13,15], "scale_marks": [35,60,80,100,120]},
				{"label": "de nourrissons 0-11 mois ayant été\nvaccinés avec le BCG, VAR, VAA, VPO3,\nDTC-Hep+Hib3 en 2013", "value": row['vac_total'] * 100, "score": row['s_vaccine'], "points": [0,5,10,12,15], "scale_marks": [55,75,100,120,150]},
				{"label": "de CSPS ayant reçu un stock de Gaz de la\nmunicipalité entre juin et décembre 2013*", "value": 0, "score": 0, "points": [0,4,6,8,10], "scale_marks": [0,1,2,3,4]}  
			]},
			{"label": "EAU ET ASSAINISSEMENT", "points": row['s_water_access'], "max_points": 18, "items": [
				{"label": "de la population avec accès à une\nsource d’eau potable fonctionnelle à\n1000m pour 300 personnes/ forage.*", "value": row['access'], "score": row['s_water_access'], "points": [0,4,8,12,18], "scale_marks": [15,35,55,75,95]}
			]},
			{"label": "ACTES DE NAISSANCES", "points": row['s_projected_births'], "max_points": 12, "items": [
				{"label": "Nombre d’actes de naissances\ndélivrés comparé aux naissances\nattendues", "value": row['projected_births_v'] * 100, "score": row['s_projected_births'], "points": [0,1,3,5,7,12], "scale_marks": [10,20,40,60,80,100]}
			]}

		]}

	j.append(ob);

totals = []
for item in j:
	totals.append( item['total_points'] )

get_stars(j, np.percentile(totals, [20,40,60,80,100]))



with open('poster2_data.json', 'w') as outfile:
  json.dump(j,outfile, indent=4, separators=(',', ': '))

