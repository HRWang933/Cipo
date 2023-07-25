MODELS used by different processing routines for creating particular Impala table structures.

    Each directory contains set of models (CREATE TABLE body expressions) for particular source file type:

ad    - Assignment XML files
pa    - Old Application XML files
pg    - Old Grant XML files
ipa   - New Application XML files
ipg   - New Grant XML files
phi   - Patent holder information (Scraped from https://fees.uspto.gov/MaintenanceFees/fees/details?)
thist - Transaction history information (Requested from https://ped.uspto.gov/api/queries)
ainf  - Application information (Requested from https://ped.uspto.gov/api/queries)
fee_d - Maintenance fee MAIN TXT file
fee_m - Maintenance fee DESCRIPTION TXT file
att   - Attorney TXT file
td    - Canada Trademarks data

    Each models script from particular directory contains body of SQL CREATE TABLE statement.
This boby used by tbl_model() class from helpers.py to construct full SQL statement.
