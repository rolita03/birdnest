from flask import Flask, render_template
import requests
import json
import xml.etree.ElementTree as ET
import ast
import logger

def get_drone_ndz():
    response = requests.get('https://assignments.reaktor.com/birdnest/drones')
    data = ET.fromstring(response.content)

    positionx =  data.findall(".//capture/drone/positionX")
    positiony =  data.findall(".//capture/drone/positionY")
    list_serial_ndz = []
    for x,y in zip(positionx,positiony):
        if (float(x.text) >= 250000 and float(y.text) >= 250000):
        #   print("Iteration")
        #   print(f'x value is {x.text}')
        #   print(f'y value is {y.text}')
          serial = data.findtext(f".//capture/drone[positionX='{x.text}']/serialNumber")
          print(f'serial number is {serial}')
          list_serial_ndz.append(serial)
        #   print(list_serial_ndz)
    return(list_serial_ndz)
    
def get_pilot_ndz(list_serial_ndz):
    # for serial in list_serial_ndz:
        response_pilot = requests.get(f"https://assignments.reaktor.com/birdnest/pilots/{list_serial_ndz}")
        data = response_pilot.json()
        return data
      

# pilots_ndz = []
# drone_serial = get_drone_ndz()
# if drone_serial is not None:
   
#     for i in drone_serial:
#       pilots = get_pilot_ndz(i) 
#       pilots_ndz.append(f"{i},{pilots['firstName']},{pilots['lastName']},{pilots['email']},{pilots['phoneNumber']}")
#       print(f'hello you are {pilots_ndz}')
#       print(f"################################")
#       print(f"Serial number of Drone - {i} ")
#       print(f"First name of Pilot: {pilots['firstName']}")
#       print(f"Last name of Pilot: {pilots['lastName']}")
#       print(f"Email  of Pilot: {pilots['email']}")
#       print(f"Phone Number of Pilot: {pilots['phoneNumber']}")


## Starting Flask code
app = Flask(__name__)

@app.route('/')


def get_data_from_api():
    drone_serial = get_drone_ndz()
    pilots_ndz = []
    if drone_serial is not None:
     for i in drone_serial:
        pilots = get_pilot_ndz(i) 
        pilots_ndz.append(f"{i},{pilots['firstName']},{pilots['lastName']},{pilots['email']},{pilots['phoneNumber']}")
        # print(pilots_ndz)
        # pilots_ndz_Serial = pilots_ndz_Serial.append(i)
        # pilots_ndz_first_name = pilots_ndz_first_name.append(pilots['firstName'])
        # pilots_ndz_last_name = pilots_ndz_last_name.append(pilots['lastName'])
        # pilots_ndz_email = pilots_ndz_email.append(pilots['email'])
        # pilots_ndz_phone_number = pilots_ndz_phone_number.append(pilots['phoneNumber'])

        # print(f"################################")
        # print(f"Serial number of Drone - {i} ")
        # print(f"First name of Pilot: {pilots['firstName']}")
        # print(f"Last name of Pilot: {pilots['lastName']}")
        # print(f"Email  of Pilot: {pilots['email']}")
        # print(f"Phone Number of Pilot: {pilots['phoneNumber']}")  
    headings = ("FirstName","LastName","Email","PhoneNumber")
    return render_template("table.html",pilots_ndz=pilots_ndz)

if __name__ == '__main__':
     app.run(debug=True)



      