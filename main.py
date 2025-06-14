import os.path
import base64
import csv
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://url']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {'raw': raw}
    sent_message = service.users().messages().send(userId='me', body=message).execute()
    return sent_message.get("id")

def load_recipients(filename):
    recipients = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append({'name': row['name'], 'email': row['email']})
    return recipients

def write_log(filename, logs):
    with open(filename, mode='w', newline='', encoding='utf-8') as logfile:
        writer = csv.writer(logfile)
        writer.writerow(['name', 'email', 'status'])
        writer.writerows(logs)

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    recipients = load_recipients('recipients.csv')

    subject = '一斉送信テスト'
    body_template = 'こんにちは、{name}さん！\n\nこれはGmail APIからの一斉送信テストです。'

    logs = []

    for recipient in recipients:
        name = recipient['name']
        email = recipient['email']
        personalized_body = body_template.format(name=name)
        try:
            message_id = send_email(service, email, subject, personalized_body)
            print(f'送信成功: {name} ({email}), Message ID: {message_id}')
            logs.append([name, email, '✅'])
        except HttpError as error:
            print(f'送信失敗: {name} ({email}), エラー: {error}')
            logs.append([name, email, '✖'])

    # ログファイルに書き出し
    write_log('log.csv', logs)
    print('ログファイル log.csv に出力しました。')

if __name__ == '__main__':
    main()
