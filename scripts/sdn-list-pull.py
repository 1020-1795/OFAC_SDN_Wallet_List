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
    'ARB': 'Ethereum',
    'OP': 'Ethereum'
}

def recognize_base_chain_from_address(address):
    if address.startswith(('1', '3', 'bc1')):
        return 'Bitcoin'
    elif address.startswith('0x'):
        return 'Ethereum'
    elif address.startswith('T'):
        return 'Tron'
    else:
        return 'Unknown'

def get_digital_currency_addresses():
    print("Starting to fetch the SDN XML file...")
    try:
        response = requests.get(SDN_XML_URL)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Successfully fetched the XML file.")
            root = ET.fromstring(response.content)
            print("Parsed the XML content.")
            
            complete_wallet_list = [] 
            blockchain_wallets = defaultdict(list)
            unrecognized_wallets = [] 
            
            for id_element in root.findall('.//ns:id', namespaces):
                id_type = id_element.find('ns:idType', namespaces)
                id_number = id_element.find('ns:idNumber', namespaces)
                
                if id_type is not None and 'Digital Currency Address' in id_type.text:
                    currency_type = id_type.text.split(' - ')[-1]
                    wallet_address = id_number.text if id_number is not None else 'N/A'
                    print(f"Currency: {currency_type}, Address: {wallet_address}")
                    
                    complete_wallet_list.append(wallet_address)
                    
                    if currency_type in currency_chain_map:
                        blockchain = currency_chain_map[currency_type]
                    else:
                        blockchain = recognize_base_chain_from_address(wallet_address)
                    
                    if blockchain != 'Unknown':
                        blockchain_wallets[blockchain].append(wallet_address)
                    else:
                        unrecognized_wallets.append(wallet_address)
            
            complete_list_file = "OFAC_Sanctioned_Wallet_Lists/1_Complete_Sanctioned_Wallet_List.txt"
            print(f"Attempting to write to {complete_list_file}...")
            with open(complete_list_file, "w") as f:
                f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                for address in complete_wallet_list:
                    f.write(f"{address}\n")
            print(f"File written successfully to {complete_list_file}.")
            
            index = 2
            for blockchain, addresses in blockchain_wallets.items():
                blockchain_file_name = f"OFAC_Sanctioned_Wallet_Lists/{index}_{blockchain}_Sanctioned_Wallet_List.txt"
                print(f"Attempting to write to {blockchain_file_name}...")
                with open(blockchain_file_name, "w") as f:
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    for address in addresses:
                        f.write(f"{address}\n")
                print(f"File written successfully to {blockchain_file_name}.")
                index += 1
            
            if unrecognized_wallets:
                unrecognized_file = f"OFAC_Sanctioned_Wallet_Lists/{index}_Unrecognized_Blockchain_Sanctioned_Wallet_List.txt"
                print(f"Attempting to write to {unrecognized_file}...")
                with open(unrecognized_file, "w") as f:
                    f.write(f"# Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
                    for address in unrecognized_wallets:
                        f.write(f"{address}\n")
                print(f"File written successfully to {unrecognized_file}.")
                    
        else:
            print(f"Failed to fetch SDN XML from the API: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

get_digital_currency_addresses()
