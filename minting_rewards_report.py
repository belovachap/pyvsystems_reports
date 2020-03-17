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


def create_minting_reward_pages(minting_rewards, html_output_directory, height, supernode_name):
    for minting_reward in minting_rewards:
        with open(f'{html_output_directory}/{minting_reward.minting_reward_id}.html', "w") as f:
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
            f.write(f'<h1>{supernode_name} Minting Rewards Report</h1>')
            f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
            f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')
            f.write(f'<h2>Minting Reward <span class="monospace">{minting_reward.minting_reward_id}</span></h2>')
            f.write(f'<p>Block Height: <span class="monospace">{minting_reward.height}</span></p>')
            f.write(f'<p>Amount: <span class="monospace">{format_as_vsys(minting_reward.amount)}</span></p>')
            f.write(f'<p>Operation Fee: <span class="monospace">{format_as_vsys(minting_reward.operation_fee)}</span></p>')
            f.write(f'<p>Interest: <span class="monospace">{format_as_vsys(minting_reward.interest)}</span></p>')
            f.write(f'<p>MAB: <span class="monospace">{format_as_vsys(minting_reward.get_mab())}</span></p>')

            f.write(f'<h2>Leases</h2>')
            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Lease ID</th>
                        <th>Address</th>
                        <th>Start Height</th>
                        <th>Stop Height</th>
                        <th>Amount</th>
                        <th>MAB</th>
                        <th>Interest</th>
                    </tr>
                '''
            )
            for lease in minting_reward.leases:
                f.write('''
                        <tr>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                        </tr>
                    '''.format(
                        lease.lease_id,
                        lease.address,
                        lease.start_height,
                        lease.stop_height,
                        format_as_vsys(lease.amount),
                        format_as_vsys(lease.get_mab(minting_reward.height)),
                        format_as_vsys(minting_reward.interest_for_lease(lease)),
                    )
                )

            f.write('</table>')
            f.write('</body></html>')


def create_index_page(minting_rewards, html_output_directory, height, supernode_name):
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
        f.write(f'<h1>{supernode_name} Minting Rewards Report</h1>')
        f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
        f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')

        f.write('<h2>Minting Rewards</h2>')
        f.write(f'<p>Total Minting Rewards: <span class="monospace">{len(minting_rewards)}</span></p>')
        f.write('<table>')
        f.write(
            '''
                <tr>
                    <th>Minting Reward ID</th>
                    <th>Height</th>
                    <th>Timestamp</th>
                    <th>Amount</th>
                    <th>Operation Fee</th>
                    <th>Interest</th>
            ''')
        for minting_reward in minting_rewards:
            f.write(
                '''
                    <tr>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                        <td class="monospace">{}</td>
                    </tr>
                '''.format(
                    f'<a href="{minting_reward.minting_reward_id}.html">{minting_reward.minting_reward_id}</a>',
                    f'{minting_reward.height}',
                    f'{datetime.fromtimestamp(minting_reward.timestamp/1000000000)}',
                    f'{format_as_vsys(minting_reward.amount)}',
                    f'{format_as_vsys(minting_reward.operation_fee)}',
                    f'{format_as_vsys(minting_reward.interest)}',
                )
            )

        f.write('</table>')
        f.write("</body></html>")


if __name__ == '__main__':
    html_output_directory = 'html_output/minting_rewards_report'
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

    block_heights = set()
    minting_rewards = set()
    for address in addresses:
        for reward in address.minting_rewards():
            block_heights.add(reward.height)
            minting_rewards.add(reward)

    # Check that we don't have minting_rewards for the same block height.
    assert len(block_heights) == len(minting_rewards)

    minting_rewards = list(minting_rewards)
    minting_rewards = sorted(minting_rewards, key=lambda x: x.height)

    create_minting_reward_pages(minting_rewards, html_output_directory, height, supernode_name)
    create_index_page(minting_rewards, html_output_directory, height, supernode_name)
