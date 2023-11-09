# ReadAllGmail - Generated in collaboration with ChatGPT - This may become a backend for a chrome extension in the future.
This utility script is designed to mark unread emails as read in your Gmail account using Python and Google's Gmail API. Please follow the setup instructions carefully before running the script.

## Prerequisites
To use this script, you must have Python installed on your system and access to the Gmail API, along with OAuth 2.0 credentials for authentication.

## Setup Instructions

### Step 1: Enable the Gmail API
To interact with Gmail, you must enable the API and obtain the necessary credentials:

1. Visit the [Google Developers Console](https://console.developers.google.com/).
2. Start a new project by clicking `Create Project`, provide a name for your project, and then click `Create`.
3. Once the project is created, navigate to the `Dashboard` section.
4. Click on `+ ENABLE APIS AND SERVICES`.
5. In the API Library, search for "Gmail API" and enable it for your project.

### Step 2: Authentication Credentials
Now you need to create and download the credentials to allow your script to access your Gmail account securely:

1. Go to the `APIs & Services > Credentials` panel in the Google Developers Console.
2. Click on `Create Credentials` and choose `OAuth client ID`.
3. If prompted, configure the consent screen, and provide the required information about your application.
4. Choose `Application type` as `Desktop app` and give it a name.
5. Upon creation, click the `Download` button next to your newly created credentials to obtain the JSON file.
6. Save this file as `credentials.json` in your project directory.

### Step 3: Install the Google Client Library
You need to install the Google client library for Python to interact with the Gmail API. Execute the following command:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## How It Works

The script automates the process of logging into the Gmail API using the provided credentials, searching for all unread messages, and iteratively removing the 'UNREAD' label from them.

## Usage

With the setup complete, you can run the script using the following command:

```bash
python main.py
```

## Important Notes

- **Caution:** Running this script will modify the read status of your emails on your Gmail account. Please use it responsibly and review the script before executing.
- **Security:** Your email data is sensitive. Keep your `credentials.json` and `token.json` files secure, and never share them.
- **Testing:** It's recommended to test the script on a small number of emails or a test account before applying it to your primary email account.
- **Errors and Rate Limits:** If you encounter any errors or rate limits from the Gmail API, the script includes an exponential backoff strategy to retry the request after a certain interval.

For further assistance or feedback, please reach out through the Issues section of this repository.

---

