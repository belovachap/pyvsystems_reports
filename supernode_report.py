from datetime import datetime

import requests

from pyvsystems_rewards.format import format_as_vsys


API_URL = 'http://wallet.v.systems/api' # mainnet

SUPERNODE_NAMES = {
    'ARBQTCYws5FZAVtA1ZFLsGhBtPymr4Hp5CX': 'Staking Club',
    'AREExiJHmLb15ePMTyajnt4wb2bD4BENsM4': 'HelloVSYS',
    'ARGNEBKqaTTvmLK2uxC3k8db33sr96zpyxf': 'OKEx Pool',
    'ARFW9By8BkDuNdnC1M4AbRN1DV4u6AMWWSw': 'ZB Group',
    'ARAyzTJewPDkTy2SgoS4GAUc6Y6ugKpL5uu': 'Huobi Pool',
    'ARKWVGHcJGLaqTDqTq2zfmHWbc9EwRyBVB5': 'Black Diamond',
    'ARCVpcq2i6rQ7kkzNeJ1jsMec6TLmC7RNHn': 'Blockchain keys',
    'ARH7qKfAfqCwFsBC34exzBGa2iTZNKrFbhy': 'Bullseye.io',
    'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK': 'Peercoin VPool',
    'ARE4NmwpsFYb1gkUnzATHQqwB6GoG4mmYS5': 'Cobo Wallet',
    'ARCXQ8R4a4B84cdcf6BrM4fXJ8SjhEM5hZG': 'V Sydney',
    'ARNK3hFsaQfGHVqD94wZxwDb6s2YfXWc1Cv': 'Staked.us',
    'ARQNgdvu82J5hMF2UiKKoygxcH8p3KbRPm7': 'Primecoin',
    'AR2qU3zyWx3TAd97W2LvRgBVmB2Hmz5285R': 'Bit City',
    'AR85PjmwmJqK69VKWcXofyjSZgahsptZfMS': 'Staking KOREA',
}

if __name__ == '__main__':

    html_output_directory = 'html_output/supernode_report'
    address = 'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK'
    all_slots_info = requests.get(f'{API_URL}/consensus/allSlotsInfo').json()
    height = all_slots_info[0]['height']
    slots = all_slots_info[1:]
    slots = filter(lambda slot: slot["mintingAverageBalance"] != 0, slots)
    slots = sorted(slots, key=lambda slot: slot["mintingAverageBalance"])

    with open(f"{html_output_directory}/index.html", "w") as f:
        f.write('<html>')
        f.write(
            '''
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
            '''
        )

        f.write('<body>')
        f.write('<h1><a href="../index.html">Peercoin VPool</a> Supernode Report</h1>')
        f.write(f'<p>Page Updated: <span class="monospace">{datetime.utcnow()}</span></p>')
        f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')

        f.write(f'<h2>Supernodes</h2>')
        f.write("<table>")
        f.write(
            '''
                <tr>
                    <th>Name</th>
                    <th>Address</th>
                    <th>Slot ID</th>
                    <th>MAB</th>
                </tr>
            '''
        )

        for slot in slots:
            f.write('''
                    <tr>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                    </tr>
                '''.format(
                    SUPERNODE_NAMES.get(slot["address"], "UNKNOWN"),
                    slot["address"],
                    slot["slotId"],
                    format_as_vsys(slot["mintingAverageBalance"]),
                )
            )

        f.write("</table>")
        f.write("</body></html>")
