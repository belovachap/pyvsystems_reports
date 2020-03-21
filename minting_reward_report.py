from datetime import datetime
from decimal import Decimal

import requests

from pyvsystems_rewards.address_factory import AddressFactory
from pyvsystems_rewards.format import format_as_vsys


UTC_NOW = datetime.utcnow()


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
            f.write(f'<h1><a href="../index.html">{supernode_name}</a> Minting Reward Report</h1>')
            f.write(f'<p>Page Updated: <span class="monospace">{UTC_NOW}</span></p>')
            f.write(f'<p>Current Block Height: <span class="monospace">{height}</span></p>')

            f.write(f'<h2>Minting Reward <span class="monospace">{minting_reward.minting_reward_id}</span></h2>')
            f.write(f'<p>Block Height: <span class="monospace">{minting_reward.height}</span></p>')
            f.write(f'<p>Timestamp: <span class="monospace">{datetime.fromtimestamp(minting_reward.timestamp/1000000000)} ({minting_reward.timestamp})</span></p>')
            f.write(f'<p>Amount: <span class="monospace">{format_as_vsys(minting_reward.amount)}</span></p>')
            f.write(f'<p>Operation Fee: <span class="monospace">{format_as_vsys(minting_reward.operation_fee)}</span></p>')
            f.write(f'<p>Interest: <span class="monospace">{format_as_vsys(minting_reward.interest)}</span></p>')

            f.write(f'<h3>Leases</h3>')
            f.write('<table>')
            f.write(
                '''
                    <tr>
                        <th>Lease ID</th>
                        <th>Address</th>
                        <th>Start Height</th>
                        <th>Stop Height</th>
                        <th>Amount</th>
                        <th>Interest</th>
                    </tr>
                '''
            )

            leases = sorted(minting_reward.leases, key=lambda x: x.address)
            for lease in leases:
                f.write('''
                        <tr>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                            <td class="monospace">{}</td>
                        </tr>
                    '''.format(
                        lease.lease_id,
                        f'<a href="../address_report/{lease.address}.html">{lease.address}</a.',
                        lease.start_height,
                        lease.stop_height,
                        format_as_vsys(lease.amount),
                        format_as_vsys(minting_reward.interest_for_lease(lease)),
                    )
                )

            f.write('</table>')
            f.write('</body></html>')


if __name__ == '__main__':
    html_output_directory = 'html_output/minting_reward_report'
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

    create_minting_reward_pages(minting_rewards, html_output_directory, height, supernode_name)
