import json
import smtplib
import pickle
import os
import requests
from datetime import datetime
from pathlib import Path

URL = "https://www2.sepa.org.uk/hydrodata/api/Level15/14869"
LIMIT = 1.75


def main():
    home = str(Path.home())
    # open and read the last reading
    try:
        with open(home + "/lastAlmondReading.txt", "r") as f:
            last_reading = float(f.read())
    except Exception:
        last_reading = 0.0

    print("Last Result = ", last_reading)

    file_name = home + "/checkAlmond.pickled"
    with open(file_name, "rb") as pickle_f:
        parameters = pickle.load(pickle_f)

    email_address_from = parameters["email_address_from"]
    email_address_to = parameters["email_address_to"]
    email_password = parameters["email_password"]

    print(f"Address from={email_address_from}")
    print(f"Address to={email_address_to}")

    data = requests.get(URL).json()
    last = data[-1]

    lasttime = datetime.strptime(last["Timestamp"], "%Y-%m-%dT%H:%M:%S").timestamp()
    lasttimets = datetime.fromtimestamp(lasttime)
    lasttimestr = lasttimets.strftime("%d/%m/%Y %H:%M:%S")

    if float(last["Value"]) >= LIMIT and float(last["Value"]) > last_reading:
        print("Increase detected...")
        with open(home + "/lastAlmondReading.txt", "w") as f:
            f.write(last["Value"])
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(email_address_from, email_password)
            connection.sendmail(
                from_addr=email_address_from,
                to_addrs=email_address_to,
                msg=f"""Subject: River Almond water level is RED

SEPA's sensors indicated the water level is {last['Value']} at {lasttimestr}
Check https://www2.sepa.org.uk/waterlevels/?sd=t&lc=14869 for details.""",
            )
    else:
        print("Nothing to do here...")

    if float(last["Value"]) < LIMIT and last_reading >0.0:
        try:
            os.remove(home + "/lastAlmondReading.txt")
            print("Deleted last reading file")
        except Exception:
            print("lastAlmondReading.txt not found")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(email_address_from, email_password)
            connection.sendmail(
                from_addr=email_address_from,
                to_addrs=email_address_to,
                msg=f"""subject:River Almond water level

SEPA's sensors indicated the water level has fallen below RED level to {last['Value']} at {lasttimestr}
Check https://www2.sepa.org.uk/waterlevels/?sd=t&lc=14869 for details.""",
            )

    print(
        f"""SEPA's sensors indicated the water level is {last['Value']} at {lasttimestr}
Check https://www2.sepa.org.uk/waterlevels/?sd=t&lc=14869 for details."""
    )


if __name__ == "__main__":
    main()
