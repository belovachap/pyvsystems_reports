'''
Run `python reports.py` to generate the reports for your supernode's rewards and
responsibilities. Output defaults to the html_output directory for easier
development ;)

Note: maybe the html_output directory should be a command line input?
Also the api_url, hot wallet address and cold wallet address.

<3,
Peercoin
'''

from datetime import datetime
from decimal import Decimal

import requests

from pyvsystems_rewards.address_factory import AddressFactory
from pyvsystems_rewards.format import format_as_vsys
from pyvsystems_rewards.minting_reward import MintingReward


UTC_NOW = datetime.utcnow()


def create_address_audit_pages(addresses, html_output_directory, height, supernode_name):
    for address in addresses:
        with open(f'{html_output_directory}/{address.address}.html', "w") as f:
            f.write("<html>")
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
            f.write("<body>")
            f.write(f'<h1><a href="../index.html">{supernode_name}</a> Address Audit Report</h1>')
            f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
            f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')

            f.write(f'<h2>Address Audit <span class="monospace">{address.address}</span></h2>')
            f.write(f'<p>Total Interest: <span class="monospace">{format_as_vsys(address.total_interest)}</span></p>')
            f.write(f'<p>Total Pool Distribution: <span class="monospace">{format_as_vsys(address.total_pool_distribution)}</span></p>')
            f.write(f'<p>Interest Owed: <span class="monospace">{format_as_vsys(address.total_interest_owed())}</span></p>')
            f.write(f'<p><a href="../address_report/{address.address}.html">Address Report</a></p>')

            # An ordered (by height) list of combined minting rewards and pool distributions
            events = list(address.minting_rewards()) + list(address.pool_distributions())
            events = sorted(events, key=lambda x: x.height)

            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Event</th>
                        <th>Height</th>
                        <th>Amount</th>
                        <th>Balance</th>
                    </tr>
                '''
            )
            balance = 0
            for event in events:
                if isinstance(event, MintingReward):
                    amount = event.interest_for_address(address)
                    balance += amount
                    f.write('''
                            <tr>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                            </tr>
                        '''.format(
                            "Interest",
                            f'<a href="../minting_reward_report/{event.minting_reward_id}.html">{event.height}</a>',
                            format_as_vsys(amount),
                            format_as_vsys(balance),
                        )
                    )
                else:
                    amount = -1 * (event.amount + event.fee)
                    balance += amount
                    f.write('''
                            <tr>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                                <td class="monospace">{}</td>
                            </tr>
                        '''.format(
                            "Distribution",
                            event.height,
                            format_as_vsys(amount),
                            format_as_vsys(balance),
                        )
                    )

            f.write('</table>')
            f.write('</body></html>')


if __name__ == '__main__':
    html_output_directory = 'html_output/address_audit_report'
    api_url = 'http://wallet.v.systems/api'
    supernode_name = 'Peercoin VPool'
    hot_wallet_address = 'AR6Gt6GXq7yPnXoFek83sQ6sCekQWbBj7YK'
    cold_wallet_address = 'ARMb6m8PLr45oGAooYzYnxb8cSC112B7KCp'
    operation_fee_percent = Decimal('0.18')
    height = requests.get(api_url + '/blocks/height').json()['height']

    factory = AddressFactory(
        api_url=api_url,
        hot_wallet_address=hot_wallet_address,
        cold_wallet_address=cold_wallet_address,
        operation_fee_percent=operation_fee_percent
    )
    addresses = factory.get_addresses()

    create_address_audit_pages(addresses, html_output_directory, height, supernode_name)
