import imaplib
import email
import json
import html2text
import os


def imap_to_json(mail_server, username, password, maxMsg=10, mailbox="INBOX"):
    mail = imaplib.IMAP4_SSL(mail_server)
    mail.login(username, password)
    mail.select(mailbox)

    _, msg_nums = mail.search(
        None, '(UNSEEN)')
    email_data = []
    converter = html2text.HTML2Text()
    converter.body_width = 0
    for msg_num in msg_nums[0].split()[0:maxMsg]:
        _, data = mail.fetch(msg_num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        email_info = {
            "from": msg["from"],
            "to": msg["to"],
            "subject": msg["subject"],
            "date": msg["date"],
            "body": ""
        }
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    email_info["body"] = part.get_payload(decode=True).decode()
                    break
        else:
            email_info["body"] = msg.get_payload(decode=True).decode()

        email_data.append(email_info)
        # Mark message as seen, perhaps should be done AFTER any downstream logic
        mail.store(msg_num.decode(
            'utf-8').replace(' ', ','), '+FLAGS', '\Seen')

    mail.close()
    mail.logout()
    print(json.dumps(email_data, indent=4))
    return json.dumps(email_data, indent=4)


if __name__ == "__main__":
    imap_to_json(os.getenv("IMAP_SERVER"), os.getenv("IMAP_USER"),
                 os.getenv('IMAP_PASS'))
