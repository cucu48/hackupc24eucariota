import machine
import time
import ntptime
import dht
import gc
import network  
import urequests
import ujson as json



led = machine.Pin(2,machine.Pin.OUT)
cagaste = machine.Pin(21,machine.Pin.OUT)
cagaste.on()
time.sleep(0.5)
cagaste.off()
d = dht.DHT11(machine.Pin(36))
sta = network.WLAN(network.STA_IF) 

if not sta.isconnected():  
  print('connecting to network...')  
  sta.active(True)  
  sta.connect('Eucariota', 'Eucariota')  
  while not sta.isconnected():  
    pass  
print('network config:', sta.ifconfig())

ntptime.host = "time.cloudflare.com"
ntptime.settime()

url = "http://192.168.8.133:8086/api/v2/write?org=Eucariota&bucket=Eucariota&precision=ms"
headers = {
    "Authorization": "Token 5uBzwilPICdTJj1rml0c428sv_vHjNovWpfENju32T30VrJEOW3hCpLMtJkrkIC9lATsRAvoqcEzGJlqaVQFQg==",
    "Content-Type": "text/plain; charset=utf-8",
    "Accept": "application/json"
            }
UPDATE_TIME_INTERVAL = 3000  # in ms 
last_update = time.ticks_ms() 


while True:
    d.measure() 
    t = d.temperature() 
    h = d.humidity()
    #Gaudeix nano!
    data = f'''
temperatura,host=esp1 celsius={t} {(time.time() + 946684800) * 1000}
humitat,host=esp1 percentatge={h} {(time.time() + 946684800) * 1000}
ram,host=esp1 free={gc.mem_free()} {(time.time() + 946684800) * 1000}
'''
    print(data)
    led.on()
    try:
        response = urequests.post(url, headers=headers, data=data)
    except:
        cagaste.on()
    else:
        print(response.text)
        response.close()
    led.off()
    
    