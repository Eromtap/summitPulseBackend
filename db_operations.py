import psycopg2

# Module to handle database operations

CONNECT = psycopg2.connect(
    user = 'postgres',
    password = 'booger123',
    host = '34.171.140.16',
    port = 5432,
    database = 'summito2'
    )


# Store 'connecting' in both pulse columns when waitiing for connection
def show_connecting():
    cur = CONNECT.cursor()
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

