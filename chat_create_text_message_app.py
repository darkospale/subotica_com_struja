from apiclient.discovery import build
from google.oauth2 import service_account

def webhook(message):

    # Specify required scopes.
    SCOPES = ['https://www.googleapis.com/auth/chat.bot']

    # Specify service account details.
    CREDENTIALS = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES)

    # Build the URI and authenticate with the service account.
    chat = build('chat', 'v1', credentials=CREDENTIALS)

    # Create a Chat message.
    result = chat.spaces().messages().create(

        # The space to create the message in.
        #
        # Replace SPACE with a space name.
        # Obtain the space name from the spaces resource of Chat API,
        # or from a space's URL.
        parent='spaces/AAAAFUb0EFI',

        # Construct message payload for Google Chat API
        body = {
            'text': message,
        }

    ).execute()