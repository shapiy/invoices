"""Export DOCX file from Google Drive."""
import logging
import os
import pickle

import httplib2
from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

DOCX_MIME_TYPE = \
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

LOGGER = logging.getLogger(__name__)


def export_docx(file_id: str, dirname: str) -> str:
    """Export DOCX file and return the filename."""
    service = _build_service()

    filename = os.path.join(dirname, '{}.docx'.format(file_id))
    request = service.files().export(   # pylint: disable=no-member
        fileId=file_id, mimeType=DOCX_MIME_TYPE)

    with open(filename, mode='wb+') as file_handle:
        downloader = MediaIoBaseDownload(file_handle, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

    LOGGER.debug('Downloaded DOCX template and saved to: %s', filename)

    return filename


def _build_service():
    credentials = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            http = httplib2.Http()
            credentials.refresh(Request(http))
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build('drive', 'v3', credentials=credentials, cache_discovery=False)
