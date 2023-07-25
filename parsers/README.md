PARSERS used by different processing routines for parsing particular XML or TXT file.

    Each directory contains set of parser. Each parser from directory corespond to particular
table model from MODELS directory.

   Parsers contains set of XPATH expression. Each of this XPATH expression correspont to
particular COLUMN in Impala table.

ad    - Assignment XML files
pa    - Old Application XML files
pg    - Old Grant XML files
ipa   - New Application XML files
ipg   - New Grant XML files
fee_d - Maintenance fee MAIN TXT file
fee_m - Maintenance fee DESCRIPTION TXT file
att   - Attorney TXT file
td    - Canada Trademarks data

   helpers.py module contains helper functions which parse particular XPATH expressions set
from particular parser.
