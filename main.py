### IMPORT ###

import sys
import json
import yaml

import pandas as pd
import datetime as dt

import click
import pyodbc

### MANAGING ARGUMENTS WITH CLICK ###

@click.command()
@click.option('--startdate', default='2019-01-01',
              help='format is YYYY-MM-DD - E.G 2019-07-26')
@click.option('--enddate', default='2020-02-01',
              help='format is YYYY-MM-DD - E.G 2019-07-26')
@click.option('--sport', default="BODY COMBAT",
help="""Main sports are listed as follows: 'CIRCUIT MINCEUR', 'NEO PILATES', 'BODY ATTACK', 'ZUMBA',
       'NEO CAF', 'CIRCUIT CORDE A SAUTER', 'BODY COMBAT', 'HIIT OLD',
       'BOOT CAMP', 'YOGA OLD', 'STEP', 'BODY SCULPT', 'CAF', 'NEO HIIT',
       'NEO STRETCH', 'ABDOS FESSIERS', 'PILATES OLD', 'BODY PUMP',
       'BODY BALANCE', 'NEO CROSS TRAINING', 'CXWORX', 'ZUMBA BURST',
       'AFRO DANCE', 'GYM ZEN', 'STRETCHING', 'NEO YOGA', 'GRIT CARDIO',
       'STEP DEBUTANT', 'POITRINE BRAS DOS', 'TONE', 'ABDOS EXPRESS',
       'AFROVIBE', 'STRONG NATION', 'NEO BOXE&ROPE', 'MIX FITNESS', 'LIA',
       "MOUV'K", 'RAGGA SESSIONS', 'CIRCUIT VENTRE PLAT', 'BODY JAM',
       'DJEMBEL', 'LIA DEBUTANT', 'NEO AFRO', 'DANSE AFRICAINE',
       'FUN DANCE', 'KUDURO FIT', 'INITIATION DANSE AFRO CARIBEENNE',
       'Zumba Débutant', 'SH BAM'""")
@click.option('--output', default='both',
              help="""Allows the user to choose the desired output type : \n
              - 'json' : export the results to a json file called 'results.json' \n
              - 'display': only display the results in terminal \n
              - 'both': export to json and display the results""")

def compute(sport, startdate, enddate, output):
        """  Computes how many students each coach has for a given sport and period of time. """

        sport = sport.upper()
        click.echo(f'startdate = {startdate} - enddate {enddate} - sport = {sport}')

        if check_date([startdate, enddate]) and check_sport(sport):
                planning_temp = planning_df.loc[planning_df['dateDebutCours'].between(startdate, enddate)].drop_duplicates()
                passage_temp = passage_df.loc[(passage_df['datePassage'].between(startdate, enddate)) & (passage_df['typePointPassage'] == 'Cours co')].drop_duplicates()
                df = (planning_temp.merge(passage_temp,
                                         left_on=['idClub', planning_temp['dateDebutCours'].dt.day],
                                         right_on = ['idClub', passage_temp['datePassage'].dt.day])
                                  .assign(diff = lambda x: (x['dateDebutCours'] - x['datePassage']).dt.total_seconds()))

                results = (df.loc[(df['activite'] == sport) & (SECONDS_BEFORE <= df['diff']) & (df['diff'] <= SECONDS_AFTER)]
                             .groupby('idCoach')
                             .agg({'idPlanning': ['count']})
                             .droplevel(0, axis=1)
                             .sort_values(by='count', ascending=False)
                             .to_dict()['count'])

                ### OUTPUT ###
                if output == 'display' or output == 'both': click.echo(json.dumps(results, indent=2))
                if output == 'json' or output == 'both':
                        with open(JSON_FILENAME, 'w') as json_file: json.dump(results, json_file, indent=2)

def end_program(msg):
        """ Displays a message and terminates program. """
        click.echo(msg)
        sys.exit()
        
def load_config(CONFIG_FILENAME):
        """ Loads configuration from the .yaml file. """
        try:
                config = yaml.safe_load(open(CONFIG_FILENAME, 'r'))
                click.echo(f'{CONFIG_FILENAME} found.')
                return config['server'], config['database'], config['username'], config['password']
        except: return False, False, False, False

def connection():
        """ Connects to the Azure database. """
        SERVER, DATABASE, USERNAME, PASSWORD = load_config(CONFIG_FILENAME)
        if SERVER != False:
                try:
                        click.echo('Attempting to connect to distant server...')
                        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
                        click.echo('Connection established. Loading data...')
                        return (pd.io.sql.read_sql('SELECT * FROM [dbo].[Passage]', cnxn),
                                pd.io.sql.read_sql('SELECT * FROM [dbo].[Planning]', cnxn))

                except: end_program(f'Failed to connect to server - program terminated')
        else: end_program(f'Failed to load {CONFIG_FILENAME} - program terminated')

def load_csv_files(PASSAGE_CSV_FILENAME, PLANNING_CSV_FILENAME):
        """ Loads CSV file. Useful in order to test and debug the program without having to wait for the data to download. """
        try:
                click.echo('Loading CSV files...')
                passage_df = pd.read_csv(PASSAGE_CSV_FILENAME)
                passage_df['datePassage'] = pd.to_datetime(passage_df['datePassage'])
                planning_df = pd.read_csv(PLANNING_CSV_FILENAME)
                planning_df['dateDebutCours'] = pd.to_datetime(planning_df['dateDebutCours'])
                return passage_df, planning_df

        except: end_program('Failed to load the CSV Files - program terminated')

def check_date(dates_list):
        """ Returns True if dates are well formated and in the right order. """
    
        for date in dates_list:
                year, month, day = date.split('-')
                try : dt.datetime(int(year),int(month),int(day))
                except: end_program('Error : date format is not valid. Please enter the date in the format YYYY-MM-DD - program terminated')
        if dt.datetime.strptime(dates_list[0], '%Y-%m-%d') < dt.datetime.strptime(dates_list[1], '%Y-%m-%d'): return True
        else: end_program('Error : The end date must be greater than the start date - program terminated.')

def check_sport(sport):
        """ Returns True if sport exists in the dataset. """
        if sport in planning_df['activite'].unique(): return True
        else: end_program('Error : sport not found in planning - program terminated')

### GLOBAL VARIABLES ###

CONFIG_FILENAME = 'config.yaml'
REMOTE = True
PASSAGE_CSV_FILENAME = 'dbo.Passage.csv'
PLANNING_CSV_FILENAME = 'dbo.Planning.csv'
SECONDS_BEFORE = -900
SECONDS_AFTER = 300
JSON_FILENAME = 'results.json'

### MAIN ###

if __name__ == '__main__':

        if REMOTE: passage_df, planning_df = connection()
        else: passage_df, planning_df = load_csv_files(PASSAGE_CSV_FILENAME, PLANNING_CSV_FILENAME)
        click.echo('Data loaded')
        compute()