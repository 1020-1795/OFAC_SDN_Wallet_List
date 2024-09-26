# OFAC_SDN_Wallet_List

This repository automatically pulls and updates a list of cryptocurrency wallets sanctioned by OFAC (Office of Foreign Assets Control) using the official OFAC API.

The list is updated daily at 4:00 UTC and contains wallets categorized by their respective blockchains.

How It Works

	•	The script pulls data directly from the OFAC API.
	•	Wallets are categorized based on blockchain or recognized patterns (e.g., Bitcoin, Ethereum, etc.).
	•	A Complete Sanctioned Wallet List is provided, along with blockchain-specific lists for easier filtering.
	•	Unrecognized wallets, if any, are placed in a separate list.

Automated Updates

	•	The wallet lists are automatically updated every day at 4:00 UTC.
	•	Changes are committed to this repository whenever there is an update.

Disclaimer

	•	This repository is provided as-is with no warranties, either express or implied.
	•	The data is directly sourced from the official OFAC API, but there is no guarantee of the accuracy, completeness, or timeliness of the data.
	•	No warranty of fitness for a particular purpose is provided, and use at your own risk.
	•	It is the user’s responsibility to verify the accuracy and legality of the data for their own use cases.
