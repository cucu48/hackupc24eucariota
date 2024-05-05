import lcddriver
from time import *

lcd = lcddriver.lcd()

lcd.lcd_display_string("Starting Up...")
sleep(1)

lcd.lcd_clear()


import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


bucket = "Eucariota"
org = "Eucariota"
token = "5uBzwilPICdTJj1rml0c428sv_vHjNovWpfENju32T30VrJEOW3hCpLMtJkrkIC9lATsRAvoqcEzGJlqaVQFQg=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()

device = 'ESP1'

while True:

  if device == 'ESP1': device = 'ESP2'
  else: device = 'ESP1'

  query = f'from(bucket:"Eucariota")\
  |> range(start: -1m)\
  |> filter(fn:(r) => r._measurement == "temperatura" or r._measurement == "humitat" or r._measurement == "ram")\
  |> filter(fn:(r) => r["host"] == "{device.lower()}")\
  '

  lcd.lcd_clear()
  result = query_api.query(org=org, query=query)

  results = []
  datavals = ["celsius", "percentatge", "free"]
  for table in result:
    for record in table.records:
      results.append((record.get_field(), record.get_value()))

  last_vals = []
  try:
    for val in datavals:
      currall = []
      for i in results:
        if i[0] == val:
          currall.append(i)
      last_vals.append(currall[-1])
      currall = []
  except:
    print(f"No data available for {device}")
    last_vals = [(0, 'ERROR'), (0, 'ERROR'), (0, 'ERROR')]
  #print("Displaying Data!")
  lcd.lcd_display_string(f"Eucariota {device} {localtime()[3]}:{localtime()[4]}")
  lcd.lcd_display_string("Temp: " + str(last_vals[0][1]) + " C", 2)
  lcd.lcd_display_string("Hum: " + str(last_vals[1][1]) + " %", 3)
  lcd.lcd_display_string("Free: " + str(last_vals[2][1]) + " B", 4)

  sleep(5)  

