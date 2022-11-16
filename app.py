from flask import Flask, render_template, request
import pickle
from errors.handlers import errors
import numpy as np
import pandas as pd

def scale(x):
  min = 1
  max = 600
  out = (x - min)/(max-min)
  return out

def assign(x):
    if x=='on':
        return 1
    else:
        return 0

def difference (list1, list2):
    diff = []
    for i in list1:
       if i not in list2:
           diff.append(i)
    return diff

post=0

def create_app():

    app = Flask(__name__)
    app.register_blueprint(errors)

    @app.route('/')
    def main():
        return render_template('index.html')

    @app.route('/',methods=['GET','POST'])
    def home():
        if request.method=="POST":
            year = request.form.get('year')
            Running_km = request.form.get('Running_km')
            mileage = request.form.get("mileage")
            engine = request.form.get("engine")
            fuel_type = request.form.get("Fuel_type")
            owners = request.form.get("owners")
            insurance = request.form.get("Insurance")
            turbo = request.form.get("Turbo")
            seat_rows = request.form.get("Seat_rows")
            brake_type = request.form.get("Brake_type")
            transmission = request.form.get("Transmission")
            cruise_control = request.form.get("Cruise_control")
            abs = request.form.get("ABS")
            parking_sensor = request.form.get("Parking_sensor")
            stearing_controls  = request.form.get("Stearing_controls")
            sunroof = request.form.get("Sunroof")
            infotainment = request.form.get("Infotainment")
            rear_wiper = request.form.get("Rear_wiper")  
        try:
            year = np.log(int(year),dtype=np.float64)
            engine = np.log(int(engine),dtype=np.float64)
            mileage = np.log(int(mileage),dtype=np.float64)
            Running_km = scale(np.sqrt(int(Running_km),dtype=np.float64))
            cruise_control = assign(cruise_control)
            abs = assign(abs)
            parking_sensor = assign(parking_sensor)
            stearing_controls = assign(stearing_controls)
            sunroof = assign(sunroof)
            infotainment = assign(infotainment)
            rear_wiper = assign(rear_wiper)
        except:
            return render_template('index.html',message = "Please fill details in Numbers",post=1)     
        
        all_details = {"Running_km":Running_km,
                        "Engine":engine,
                        "Cruise_Control":cruise_control,
                        "ABS":abs,
                        "Sunroof":sunroof,
                        "Rear_Wiper":rear_wiper,
                        "Parking_Sensors":parking_sensor,
                        "Steering_controls":stearing_controls,
                        "Infotainment_screen":infotainment,
                        "Mileage":mileage,
                        "year":year,
                        "Fuel":fuel_type,
                        "Owners":owners,
                        "Insurance":insurance,
                        "Turbo":turbo,
                        "Seat_rows":seat_rows,
                        "Rear Brake Type":brake_type,
                        "Transmission_Type":transmission}
        
        df = pd.DataFrame(all_details,index=[0])
        X_deploy_enc = pd.get_dummies(df)
        ref_cols = pickle.load(open('columns.pkl','rb'))
        deploy_cols = X_deploy_enc.columns
        print(ref_cols)
        print(deploy_cols)
        missing_cols = difference(ref_cols,deploy_cols)
        for cols in missing_cols:
            X_deploy_enc[cols] = 0
        X_deploy_enc = X_deploy_enc[ref_cols]
        model = pickle.load(open('model.pkl','rb'))
        result = model.predict(X_deploy_enc)    
        result = np.exp(result)

        return render_template('index.html',message = "Predicted Price of the Car ₹ "+str(np.round_(result[0],decimals=0)),post=1)
 
# if __name__== "__main__" :
#      app.run()          
create_app()