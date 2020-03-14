from datetime import datetime
import requests


API_URL = 'http://wallet.v.systems/api' # mainnet


if __name__ == '__main__':

    html_output_directory = 'html_output'
    address = 'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK'
    mab = requests.get(f'{API_URL}/consensus/mintingAverageBalance/{address}').json()

    with open(f"{html_output_directory}/index.html", "w") as f:
        f.write("<html><body>")

        f.write("<h1>Peercoin VPool Supernode</h1>")
        f.write("<p>Page updated: {}</p>".format(datetime.utcnow()))
        f.write("<p>Blockchain height: {}</p>".format(mab["height"]))
        f.write("<p>Address: {}</p>".format(address))
        f.write("<p>MAB: {}</p>".format(mab["mintingAverageBalance"]))

        f.write("<h2>Reports</h2>")
        f.write("<p><ul>")
        f.write('<li><a href="mab_report/">MAB Report</a></li>')
        f.write('<li><a href="rewards_report/">Rewards Report</a></li>')
        f.write("</ul></p>")

        f.write("</body></html>")
