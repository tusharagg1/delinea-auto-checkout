# Delinea Auto Checkout

Automation for [Delinea Secret Server](https://delinea.com/) built with Selenium and the Secret Server REST API.

## Scripts

- **`checkin_checkout.py`** — logs into Secret Server via Selenium (headless Chrome) and performs an automated **check-out** then **check-in** of a given secret ID.
- **`failed_hearbeat.py`** — queries the Secret Server REST API and returns the IDs of secrets whose last heartbeat failed (`Failed`, `UnableToConnect`, `AccountLockedOut`, `UnknownError`) across a configured set of secret templates.

## Setup

```bash
pip install selenium webdriver-manager python-dotenv requests pandas
```

Create a git-ignored `.env` with:

```
LOGIN_SITE=<secret server login url>
API_SITE=<secret server base url>
EMAIL=<username>
PASSWD=<password>
API_TOKEN=<secret server api bearer token>
```

## Run

```bash
python checkin_checkout.py
python failed_hearbeat.py
```
