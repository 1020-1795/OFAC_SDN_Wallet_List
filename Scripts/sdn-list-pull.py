import requests
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime

# URL to fetch the SDN XML directly from the API
SDN_XML_URL = 'https://sanctionslistservice.ofac.treas.gov/api/download/sdn.xml'

# Namespace dictionary to handle the XML namespaces
namespaces = {
    'ns': 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/XML'
}

# Blockchain categorization map based on currency type (direct mapping)
# Layer 2 chains like Arbitrum and Optimism are mapped to their base layer, Ethereum.
currency_chain_map = {
    'BTC': 'Bitcoin',
    'XBT': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Smart Chain',
    'TRX': 'Tron',
    'XRP': 'Ripple',
    'SOL': 'Solana',
    'DOT': 'Polkadot',
    'AVAX': 'Avalanche',
    'MATIC': 'Polygon',
    'ALGO': 'Algorand',
    'XLM': 'Stellar',
    'ARB': 'Ethereum',  # Arbitrum mapped to Ethereum
    'OP': 'Ethereum',   # Optimism mapped to Ethereum
    # Add more base chains if necessary
}

# Function to recognize base chain from address patterns
def recognize_base_chain_from_address(address):
    if address.startswith(('1', '3', 'bc1')):
        return 'Bitcoin'
    elif address.startswith('0x'):
        return 'Ethereum'
    elif address.startswith('T'):
        return 'Tron'
    else:
        return 'Unknown'

# Function to fetch, parse, and output digital currency addresses
def get_digital_currency_addresses():
    print("Starting to fetch the SDN XML file...")  # Debugging output
    try:
        # Step 1: Fetch the SDN XML file from the API
        response = requests.get(SDN_XML_URL)
        print(f"Response status code: {response.status_code}")  # Debugging output
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Successfully fetched the XML file.")  # Debugging output

            # Step 2: Parse the XML content from the API response, handling namespaces
            root = ET.fromstring(response.content)
            print("Parsed the XML content.")  # Debugging output
            
            # Step 3: Initialize dictionaries to store wallet data
            complete_wallet_list = []  # For storing all wallets
            blockchain_wallets = defaultdict(list)  # For storing wallets per blockchain
            unrecognized_wallets = []  # For storing unrecognized wallets
            
            # Loop through each 'id' element using the namespace
            for id_element in root.findall('.//ns:id', namespaces):
                # Find the idType and idNumber elements within each 'id', using namespaces
                id_type = id_element.find('ns:idType', namespaces)
                id_number = id_element.find('ns:idNumber', namespaces)
                
                # Check if idType contains 'Digital Currency Address'
                if id_type is not None and 'Digital Currency Address' in id_type.text:
                    # Extract the blockchain type (ETH, BTC, etc.) and wallet address
                    currency_type = id_type.text.split(' - ')[-1]  # Get the currency type (e.g., BTC, ETH)
                    wallet_address = id_number.text if id_number is not None else 'N/A'
                    print(f"Currency: {currency_type}, Address: {wallet_address}")  # Debugging output
                    
                    # Add wallet to the complete list
                    complete_wallet_list.append(wallet_address)
                    
                    # Step 1: Check if currency is a base layer blockchain (ignoring Layer 2s)
                    if currency_type in currency_chain_map:
                        blockchain = currency_chain_map[currency_type]
                    else:
                        # Step 2: Try to recognize the blockchain from the address pattern
                        blockchain = recognize_base_chain_from_address(wallet_address)
                    
                    # Step 3: If recognized, add to the corresponding blockchain, else add to unrecognized
                    if blockchain != 'Unknown':
                        blockchain_wallets[blockchain].append(wallet_address)
                    else:
                        unrecognized_wallets.append(wallet_address)
            
            # Step 4: Write the Complete Sanctioned Wallet List
            complete_list_file = "OFAC Sanctioned Wallet Lists/1_Complete_Sanctioned_Wallet_List.txt"
            print(f"Attempting to write to {complete_list_file}...")  # Debugging output
            with open(complete_list_file, "w") as f:
                # Write the "Last Updated" timestamp
                f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                # Write all wallets, one per line
                for address in complete_wallet_list:
                    f.write(f"{address}\n")
            print(f"File written successfully to {complete_list_file}.")  # Debugging output
            
            # Step 5: Write individual blockchain files (only for blockchains with wallets)
            index = 2
            for blockchain, addresses in blockchain_wallets.items():
                blockchain_file_name = f"OFAC Sanctioned Wallet Lists/{index}_{blockchain}_Sanctioned_Wallet_List.txt"
                print(f"Attempting to write to {blockchain_file_name}...")  # Debugging output
                with open(blockchain_file_name, "w") as f:
                    # Write the "Last Updated" timestamp
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    # Write each wallet address for that blockchain
                    for address in addresses:
                        f.write(f"{address}\n")
                print(f"File written successfully to {blockchain_file_name}.")  # Debugging output
                index += 1
            
            # Step 6: Write unrecognized wallets if any
            if unrecognized_wallets:
                unrecognized_file = "OFAC Sanctioned Wallet Lists/Unrecognized_Blockchain_Sanctioned_Wallet_List.txt"
                print(f"Attempting to write to {unrecognized_file}...")  # Debugging output
                with open(unrecognized_file, "w") as f:
                    # Write the "Last Updated" timestamp
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    for address in unrecognized_wallets:
                        f.write(f"{address}\n")
                print(f"File written successfully to {unrecognized_file}.")  # Debugging output
                    
        else:
            print(f"Failed to fetch SDN XML from the API: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function to fetch and output digital currency addresses immediately
get_digital_currency_addresses()
