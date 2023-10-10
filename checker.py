import os, csv, re, time, requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

smtp_domain = os.getenv('SMTP_DOMAIN')
smtp_api_key = os.getenv('SMTP_API_KEY')
smtp_from = os.getenv('SMTP_FROM')
smtp_to = os.getenv('SMTP_TO')
renew_days = int(os.getenv('RENEW_DAYS', 15))

def check_ssl(domain):
    endpoint = "https://www.sslchecker.com/sslchecker"
    payload = {'SslCheckerForm[url]': domain, 'SslCheckerForm[port]': '443', 'yt0': ''}
    response = requests.post(endpoint, data=payload)
    return response.text

def send_email(message):
    if smtp_domain != None and smtp_api_key != None and smtp_from != None and smtp_to != None:
        endpoint = "https://api.mailgun.net/v3/" + smtp_domain + "/messages"
        auth = ("api", smtp_api_key)
        payload = {"from": smtp_from, "to": smtp_to, "subject": "SSL Checker", "text": message}
        response = requests.post(endpoint, auth=auth, data=payload)
        return response.text
    else:
        return "SMTP config not found in your ENV file"

def days_between(start_date, end_date):
    return abs((end_date - start_date).days)

if __name__ == "__main__":
    rows = list()
    email_message = ""
    fileName = "domains.csv"
    # parse csv file
    with open(fileName) as file:
        reader = csv.reader(file)
        for row in reader: # [domain, expires, errors]
            domain = row[0]
            try:
                # check if date expires
                if len(row) > 1:
                    expires_date = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                    if expires_date > datetime.today() and days_between(datetime.today(), expires_date) > renew_days:
                        rows.append(row)
                        continue
                # get expiration date
                regex = r"<input(.*?)id=\"inpExpireDate\"(.*)value=\"(.*?)\""
                match = re.search(regex, check_ssl(domain))
                expires = match.group(3)
                row[1] = expires
                rows.append(row)
                email_message = email_message + "\n" + domain + ": " + expires
                print(domain, expires)
                time.sleep(30)
            except BaseException as e:
                err_message = str(e)
                row[2] = err_message
                rows.append(row)
                email_message = email_message + "\n" + domain + ": " + err_message
                print(domain, err_message)
    # save updates to csv
    # with open(fileName, 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(rows)
    # send email
    # if email_message != "":
        # send_email(email_message)
    print('DONE')
