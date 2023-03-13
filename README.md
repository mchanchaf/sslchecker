
# SSL Checker

Check domains SSL certificates expiration date from csv file

## Installation

1. Install dependencies

```bash
  pip install python-dotenv
```

2. Clone git repository

```bash
  git clone https://github.com/mchanchaf/sslchecker.git
```
    
3. Rename .env.local to .env and change **mailgun** SMTP settings (only if you want to receive logs via email)

4. Create a file **domains.csv** without **headers** and put domains to scan (domain per line)

## Usage

Run the following command and wait until it end

```bash
  python3 checker.py
```

The script will update the **domains.csv** file with expirations dates and errors (if any)
