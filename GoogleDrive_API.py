import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class GoogleDrive_API:
    def __init__(self, SERVICE_ACCOUNT_FILE_path: str = ""):
        self.SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.PARENT_FOLDER_ID = "1r-MlnEpWHx3b1fxHDnHcZ2-Wh_Y89676"

        self.service = self.authenticate(SERVICE_ACCOUNT_FILE_path)
        self.delete_all_files()

    def authenticate(self, SERVICE_ACCOUNT_FILE):
        if len(SERVICE_ACCOUNT_FILE) > 0:
            if not os.path.exists(SERVICE_ACCOUNT_FILE):
                raise rf"Google SERVICE_ACCOUNT_FILE Not Found, Path = {SERVICE_ACCOUNT_FILE}"

            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
            )
        else:
            service_account_info = {
                "type": "service_account",
                "project_id": os.environ["project_id"],
                "private_key_id": os.environ["private_key_id"],
                "private_key": os.environ["private_key"],
                "client_email": os.environ["client_email"],
                "client_id": os.environ["client_id"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": os.environ["client_x509_cert_url"],
                "universe_domain": "googleapis.com",
            }

            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.SCOPES
            )

        service = build("drive", "v3", credentials=credentials)
        return service

    def get_files(self):
        # List all files in the folder
        results = (
            self.service.files()
            .list(
                q=f"'{self.PARENT_FOLDER_ID}' in parents and trashed=false",
                fields="files(id, name)",
            )
            .execute()
        )
        return results.get("files", [])

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def delete_all_files(self):
        items = self.get_files()

        # Delete each file
        for item in items:
            file_id = item["id"]
            self.delete_file(file_id)

    def upload_file(self, file_name: str, file_path: str):
        file_metadata = {
            "name": file_name,
            "parents": [self.PARENT_FOLDER_ID],
        }
        media = MediaFileUpload(file_path)
        self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        print(rf"{file_path} uploaded.")

    def download_file(self, file_name: str, file_path: str):
        results = (
            self.service.files()
            .list(
                q=f"'{self.PARENT_FOLDER_ID}' in parents and name='{file_name}' and trashed=false",
                fields="files(id)",
            )
            .execute()
        )
        items = results.get("files", [])

        if items:
            # Get the file ID
            file_id = items[0]["id"]

            request = self.service.files().get_media(fileId=file_id)

            with open(file_path, "wb") as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%.")
        else:
            print(rf"{file_name} is Not Found")
