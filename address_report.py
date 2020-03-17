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


UTC_NOW = datetime.utcnow()


def format_as_vsys(amount):
    amount = int(amount)
    whole = int(amount / 100000000)
    fraction = amount % 100000000
    return f'{whole}.{str(fraction).ljust(8, "0")}'


def create_address_pages(addresses, html_output_directory, height, supernode_name):
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
            f.write(f'<h1>{supernode_name} Rewards Report</h1>')
            f.write(f'<h2>Address <span class="monospace">{address.address}</span></h2>')
            f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
            f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')
            f.write(f'<p>Total Interest: <span class="monospace">{format_as_vsys(address.total_interest)}</span></p>')
            f.write(f'<p>Total Pool Distribution: <span class="monospace">{format_as_vsys(address.total_pool_distribution)}</span></p>')
            f.write(f'<p>Interest Owed: <span class="monospace">{format_as_vsys(address.total_interest_owed())}</span></p>')

            f.write(f'<h2>Active Leases</h2>')
            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Lease ID</th>
                        <th>Amount</th>
                        <th>Start Height</th>
                        <th>Total Interest</th>
                    </tr>
                '''
            )
            for lease in address.active_leases(height):
                f.write('''
                        <tr>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                        </tr>
                    '''.format(
                        lease.lease_id,
                        format_as_vsys(lease.amount),
                        lease.start_height,
                        format_as_vsys(lease.total_interest),
                    )
                )

            f.write('</table>')

            f.write(f'<h2>Inactive Leases</h2>')
            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Lease ID</th>
                        <th>Amount</th>
                        <th>Start Height</th>
                        <th>Stop Height</th>
                        <th>Total Interest</th>
                    </tr>
                '''
            )
            for lease in address.inactive_leases(height):
                f.write('''
                        <tr>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                        </tr>
                    '''.format(
                        lease.lease_id,
                        format_as_vsys(lease.amount),
                        lease.start_height,
                        lease.stop_height,
                        format_as_vsys(lease.total_interest),
                    )
                )

            f.write('</table>')

            f.write(f'<h2>Pool Distributions</h2>')
            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Height</th>
                        <th>Pool Distribution ID</th>
                        <th>Amount</th>
                        <th>Fee</th>
                    </tr>
                '''
            )
            for pool_distribution in address.pool_distributions():
                f.write(
                    '''
                        <tr>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                        </tr>
                    '''.format(
                        pool_distribution.height,
                        pool_distribution.pool_distribution_id,
                        format_as_vsys(pool_distribution.amount),
                        format_as_vsys(pool_distribution.fee),
                    )
                )

            f.write('</table>')
            f.write('</body></html>')


def create_index_page(factory, html_output_directory, height, supernode_name):
    with open(f'{html_output_directory}/index.html', 'w') as f:
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
        f.write(f'<h1>{supernode_name} Rewards Report</h1>')
        f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
        f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')
        f.write(f'<p>Total Interest: <span class="monospace">{format_as_vsys(factory.total_interest)}</span></p>')
        f.write(f'<p>Total Operation Fee: <span class="monospace">{format_as_vsys(factory.total_operation_fee)}</span></p>')
        f.write(f'<p>Total Pool Distribution: <span class="monospace">{format_as_vsys(factory.total_pool_distribution)}</span></p>')
        f.write(f'<p>Total Interest Owed: <span class="monospace">{format_as_vsys(factory.total_interest-factory.total_pool_distribution)}</span></p>')

        f.write('<h2>Lenders</h2>')
        f.write('<table>')
        f.write(
            '''
                <tr>
                    <th>Address</th>
                    <th>Total Interest</th>
                    <th>Total Pool Distribution</th>
                    <th>Total Interest Owed</th></tr>
            ''')
        for address in factory.get_addresses():
            f.write(
                '''
                    <tr>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                    </tr>
                '''.format(
                    f'<a href="{address.address}.html">{address.address}</a>',
                    format_as_vsys(address.total_interest),
                    format_as_vsys(address.total_pool_distribution),
                    format_as_vsys(address.total_interest_owed()),
                )
            )

        f.write('</table>')
        f.write("</body></html>")


if __name__ == '__main__':
    html_output_directory = 'html_output/address_report'
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
    create_address_pages(addresses, html_output_directory, height, supernode_name)
    create_index_page(factory, html_output_directory, height, supernode_name)
