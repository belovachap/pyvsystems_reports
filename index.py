from datetime import datetime

import requests

from pyvsystems_rewards.format import format_as_vsys


API_URL = 'http://wallet.v.systems/api' # mainnet


if __name__ == '__main__':

    html_output_directory = 'html_output'
    address = 'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK'
    mab = requests.get(f'{API_URL}/consensus/mintingAverageBalance/{address}').json()

    with open(f"{html_output_directory}/index.html", "w") as f:
        f.write('<html>')

        f.write('''
            <style>
                table {
                    border-collapse: collapse;
                }

                table, th, td {
                    border: 1px solid black;
                }

                td {
                    padding: 10px;
                }

                .monospace {
                    font-family: "Courier New", Courier, monospace;
                }

                td.monospace {
                    text-align: right;
                }
            </style>
        ''')
        f.write('<body>')

        f.write('<h1><a href="index.html">Peercoin VPool</a> Reports</h1>')
        f.write(f'<p>Page Updated: <span class="monospace">{datetime.utcnow()}</span></p>')
        f.write(f'<p>Current Block Height: <span class="monospace">{mab["height"]}</span></p>')
        f.write(f'<p>Peercoin VPool Address: <span class="monospace">{address}</span></p>')
        f.write(f'<p>Peercoin VPool MAB: <span class="monospace">{format_as_vsys(mab["mintingAverageBalance"])}</span></p>')

        f.write("<h2>Reports</h2>")
        f.write("<p><ul>")
        f.write('<li><a href="supernode_report/index.html">Supernode Report</a></li>')
        f.write('<li><a href="address_report/index.html">Address Report</a></li>')
        f.write("</ul></p>")

        f.write("</body></html>")
