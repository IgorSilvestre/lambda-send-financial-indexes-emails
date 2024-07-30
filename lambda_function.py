import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from mailersend import emails


def lambda_handler(event, context):
    load_dotenv()
    SUBSCRIBERS = os.getenv('SUBSCRIBERS', '').split(';')
    mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

    def get_index_value(url):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        index_values = soup.find_all('p', class_='card-indice-numero')
        if len(index_values) > 1:
            index_value_text = index_values[1].get_text(strip=True)
            return index_value_text
        else:
            return 'Value not found'

    def send_email(ipca_value, cdi_value, igpm_value, selic_value, subscribers=[]):
        subject = "Índices Financeiros Atualizados"
        html = (
            f"<strong>IPCA</strong>: {ipca_value}<br>"
            f"<strong>CDI</strong>: {cdi_value}<br>"
            f"<strong>IGPM</strong>: {igpm_value}<br>"
            f"<strong>SELIC</strong>: {selic_value}<br>"
        )
        my_mail = "financeiro@gtrinvestimentos.com.br"

        for recipient in subscribers:
            response = mailer.send(
                {
                    "from": {"email": my_mail},
                    "to": [{"email": recipient}],
                    "subject": subject,
                    "html": html,
                }
            )
            print(f"Email sent to {recipient}: {response}")

    # URLs for IPCA, CDI, IGPM, and SELIC
    ipca_url = 'https://paineldeindices.com.br/indice/ipca/'
    cdi_url = 'https://paineldeindices.com.br/indice/cdi-mensal/'
    igpm_url = 'https://paineldeindices.com.br/indice/igpm/'
    selic_url = 'https://paineldeindices.com.br/indice/selic-mensal/'

    # Fetch values
    ipca_value = get_index_value(ipca_url)
    cdi_value = get_index_value(cdi_url)
    igpm_value = get_index_value(igpm_url)
    selic_value = get_index_value(selic_url)

    # Send the email
    send_email(ipca_value, cdi_value, igpm_value, selic_value, SUBSCRIBERS)

    return {
        'statusCode': 200,
        'body': 'Emails sent successfully'
    }
