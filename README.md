# Panga

## Prerequisite

Python 3+

## Installation

```shell
git clone git@github.com:lxxdn/Panga.git
cd Panga
pip install -r requirements.txt

cp secrets.example.yml secrets.yml
```

Then fill the email credentials:

1. receiver is the mailbox which you send your notice
2. notifier is the mail server which will send you notification

```shell
python panga.py
```