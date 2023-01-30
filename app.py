from flask import Flask, request, render_template
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
import pycountry
from phonenumbers.phonenumberutil import region_code_for_country_code
from phonenumbers.phonenumberutil import region_code_for_number
from opencage.geocoder import OpenCageGeocode
import folium
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_text():
    text = request.form['text']
    # Do the parsing here
    parsed_text = parse(text)
    return render_template('parsed_text.html', parsed_text=parsed_text)

def parse(text):
    # Your parsing logic here
    resp = generate_phone_code(text)
    print(resp)
    return resp





def generate_phone_code(prompt):
    if os.path.exists("mylocation.html"):
      os.remove("mylocation.html")
    try:
      number = prompt
      pn = phonenumbers.parse(number)

      country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
      location = country.name
      print(location)

      print(carrier.name_for_number(phonenumbers.parse(number), "en"))

      key = "ec657f00dd2c4231acf5820091468c13"
      geocoder = OpenCageGeocode(key)
      query = str(location)
      results = geocoder.geocode(query)
      lat = results[0]['geometry']['lat']
      lng = results[0]['geometry']['lng']
      print(lat,lng)

      myMap = folium.Map(location=[lat , lng], zoom_start=9)
      folium.Marker([lat,lng],popup=location).add_to(myMap)
      myMap.save("mylocation.html")
      os.system("mylocation.html")
      response_data = {
        'country':country,
        "location": location

      }
      return response_data
    except:
        print("Missing or invalid number\nPlease enter your phone number with country code")
        return 'error'


if __name__ == '__main__':
    app.run(debug=True)
