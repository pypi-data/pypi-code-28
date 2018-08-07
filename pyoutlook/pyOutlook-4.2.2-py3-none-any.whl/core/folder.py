import requests

from pyOutlook.internal.utils import check_response

__all__ = ['Folder']


class Folder(object):
    """An object representing a Folder in the OutlookAccount provided.

    Attributes:
        account: The :class:`OutlookAccount <pyOutlook.core.main.OutlookAccount>` this folder should be associated with
        id: The static id generated by Outlook to identify this folder.
        folder_name: The name of this folder as displayed in the account
        parent_id: The id of the folder which houses this Folder object
        child_folder_count: The number of child folders inside this Folder
        unread_count: The number of unread messages inside this Folder
        total_items: A sum of all items inside Folder

    """
    def __init__(self, account, folder_id, folder_name, parent_id, child_folder_count, unread_count, total_items):
        self.account = account
        self.parent_id = parent_id
        self.child_folder_count = child_folder_count
        self.unread_count = unread_count
        self.total_items = total_items
        self.name = folder_name
        self.id = folder_id

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)
        
    @property
    def headers(self):
        return {"Authorization": "Bearer " + self.account.access_token, "Content-Type": "application/json"}
    
    @classmethod
    def _json_to_folder(cls, account, json_value):
        return Folder(account, json_value['Id'], json_value['DisplayName'], json_value['ParentFolderId'],
                      json_value['ChildFolderCount'], json_value['UnreadItemCount'], json_value['TotalItemCount'])

    @classmethod
    def _json_to_folders(cls, account, json_value):
        return [cls._json_to_folder(account, folder) for folder in json_value['value']]

    def rename(self, new_folder_name):
        """Renames the Folder to the provided name.

        Args:
            new_folder_name: A string of the replacement name.

        Raises:
            AuthError: Raised if Outlook returns a 401, generally caused by an invalid or expired access token.

        Returns:
            A new Folder representing the folder with the new name on Outlook.

        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id
        payload = '{ "DisplayName": "' + new_folder_name + '"}'

        r = requests.patch(endpoint, headers=headers, data=payload)

        if check_response(r):
            return_folder = r.json()
            return self._json_to_folder(self.account, return_folder)

    def get_subfolders(self):
        """Retrieve all child Folders inside of this Folder.

        Raises:
            AuthError: Raised if Outlook returns a 401, generally caused by an invalid or expired access token.

        Returns:
            List[:class:`Folder <pyOutlook.core.folder.Folder>`]
        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id + '/childfolders'

        r = requests.get(endpoint, headers=headers)

        if check_response(r):
            return self._json_to_folders(self.account, r.json())

    def delete(self):
        """Deletes this Folder.

        Raises:
            AuthError: Raised if Outlook returns a 401, generally caused by an invalid or expired access token.

        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id

        r = requests.delete(endpoint, headers=headers)

        check_response(r)

    def move_into(self, destination_folder):
        # type: (Folder) -> Folder
        """Move the Folder into a different folder.

        This makes the Folder provided a child folder of the destination_folder.

        Raises:
            AuthError: Raised if Outlook returns a 401, generally caused by an invalid or expired access token.

        Args:
            destination_folder: A :class:`Folder <pyOutlook.core.folder.Folder>` that should become the parent

        Returns:
            A new :class:`Folder <pyOutlook.core.folder.Folder>` that is now
            inside of the destination_folder.

        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id + '/move'
        payload = '{ "DestinationId": "' + destination_folder.id + '"}'

        r = requests.post(endpoint, headers=headers, data=payload)

        if check_response(r):
            return_folder = r.json()
            return self._json_to_folder(self.account, return_folder)

    def copy_into(self, destination_folder):
        # type: (Folder) -> Folder
        """Copies the Folder into the provided destination folder.

        Raises:
            AuthError: Raised if Outlook returns a 401, generally caused by an invalid or expired access token.

        Args:
            destination_folder: The Folder that this Folder should be copied to.

        Returns:
            A new :class:`Folder <pyOutlook.core.folder.Folder>` representing the newly created folder.

        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id + '/copy'
        payload = '{ "DestinationId": "' + destination_folder.id + '"}'

        r = requests.post(endpoint, headers=headers, data=payload)

        if check_response(r):
            return_folder = r.json()
            return self._json_to_folder(self.account, return_folder)

    def create_child_folder(self, folder_name):
        """Creates a child folder within the Folder it is called from and returns the new Folder object.

        Args:
            folder_name: The name of the folder to create

        Returns: :class:`Folder <pyOutlook.core.folder.Folder>`
        """
        headers = self.headers
        endpoint = 'https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id + '/childfolders'
        payload = '{ "DisplayName": "' + folder_name + '"}'

        r = requests.post(endpoint, headers=headers, data=payload)

        if check_response(r):
            return_folder = r.json()
            return self._json_to_folder(self.account, return_folder)
        
    def messages(self):
        """ Retrieves the messages in this Folder, 
        returning a list of :class:`Messages <pyOutlook.core.message.Message>`."""
        headers = self.headers
        r = requests.get('https://outlook.office.com/api/v2.0/me/MailFolders/' + self.id + '/messages', headers=headers)
        check_response(r)
        from pyOutlook.core.message import Message
        return Message._json_to_messages(self.account, r.json())


