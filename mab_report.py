from datetime import datetime
import requests


API_URL = 'http://wallet.v.systems/api' # mainnet


if __name__ == '__main__':

    html_output_directory = 'html_output/mab_report'
    address = 'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK'
    slots = requests.get(f'{API_URL}/consensus/allSlotsInfo').json()[1:]
    slots = filter(lambda slot: slot["mintingAverageBalance"] != 0, slots)
    slots = sorted(slots, key=lambda slot: slot["mintingAverageBalance"])

    with open(f"{html_output_directory}/index.html", "w") as f:
        f.write("<html><body>")

        f.write("<h1>MAB Report</h1>")
        f.write("<p>Page updated: {}</p>".format(datetime.utcnow()))
        f.write("<table>")
        f.write("<tr><th>Address</th><th>Slot ID</th><th>MAB</th></tr>")
        for slot in slots:
            f.write("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                slot["address"],
                slot["slotId"],
                slot["mintingAverageBalance"],
            ))
        f.write("</table>")

        f.write("</body></html>")
