import psycopg2
import yaml

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)
# Module to handle database operations

CONNECT = psycopg2.connect(
    user = config['db_creds']['user'],
    password = config['db_creds']['password'],
    host = config['db_creds']['host'],
    port = config['db_creds']['port'],
    database = config['db_creds']['database']
    )


# Store 'connecting' in appropriate pulse columns when waitiing for connection
def show_connecting(sensor='all'):
    cur = CONNECT.cursor()
    if sensor == 'pulse1':
        cur.execute('''UPDATE heart_rates SET pulse1 = 'Connecting';''')
    elif sensor == 'pulse2':
        cur.execute('''UPDATE heart_rates SET pulse2 = 'Connecting';''')
    else:
        cur.execute('''UPDATE heart_rates SET pulse1 = 'Connecting', pulse2 = 'Connecting';''')        
    CONNECT.commit()
    
    
# Update heart rate for appropriate pulse sensor
def update_heart_rate(name, heart_rate):
    cur = CONNECT.cursor()
    if name == 'pulse1':
        cur.execute(''' UPDATE heart_rates set pulse1 = %s;''', (heart_rate,))
    if name == 'pulse2':
        cur.execute(''' UPDATE heart_rates set pulse2 = %s;''', (heart_rate,))       
    CONNECT.commit()
    
    

