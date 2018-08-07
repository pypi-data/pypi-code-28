#_  __
# | |/ /___ ___ _ __  ___ _ _ ®
# | ' </ -_) -_) '_ \/ -_) '_|
# |_|\_\___\___| .__/\___|_|
#              |_|
#
# Keeper Commander
# Copyright 2018 Keeper Security Inc.
# Contact: ops@keepersecurity.com
#

import os
import argparse
import json
import requests
import base64

from Cryptodome.Cipher import AES

from .. import generator, api, display
from ..subfolder import BaseFolderNode, find_folders, try_resolve_path
from .base import raise_parse_exception, suppress_exit, user_choice, Command


def register_commands(commands, aliases, command_info):
    commands['add'] = RecordAddCommand()
    commands['rm'] = RecordRemoveCommand()
    commands['search'] = SearchCommand()
    commands['list'] = RecordListCommand()
    commands['list-sf'] = RecordListSfCommand()
    commands['list-team'] = RecordListTeamCommand()
    commands['get'] = RecordGetUidCommand()
    commands['append-notes'] = RecordAppendNotesCommand()
    commands['download-attachment'] = RecordDownloadAttachmentCommand()
    aliases['a'] = 'add'
    aliases['s'] = 'search'
    aliases['l'] = 'list'
    aliases['lsf'] = 'list-sf'
    aliases['lt'] = 'list-team'
    aliases['g'] = 'get'
    aliases['an'] = 'append-notes'
    aliases['da'] = 'download-attachment'

    for p in [search_parser, list_parser, get_info_parser, add_parser, rm_parser, append_parser, download_parser]:
        command_info[p.prog] = p.description
    command_info['list-sf|lsf'] = 'Display all shared folders'
    command_info['list-team|lt'] = 'Display all teams'


add_parser = argparse.ArgumentParser(prog='add|a', description='Add record')
add_parser.add_argument('--login', dest='login', action='store', help='login name')
add_parser.add_argument('--pass', dest='password', action='store', help='password')
add_parser.add_argument('--url', dest='url', action='store', help='url')
add_parser.add_argument('--notes', dest='notes', action='store', help='notes')
add_parser.add_argument('--custom', dest='custom', action='store', help='comma separated key-value pairs')
add_parser.add_argument('--folder', dest='folder', action='store', help='folder path or UID where record is to be created')
add_parser.add_argument('-f', '--force', dest='force', action='store_true', help='do not prompt for omitted fields')
add_parser.add_argument('-g', '--generate', dest='generate', action='store_true', help='generate random password')
add_parser.add_argument('title', type=str, action='store', help='record title')
add_parser.error = raise_parse_exception
add_parser.exit = suppress_exit


rm_parser = argparse.ArgumentParser(prog='rm', description='Remove record')
rm_parser.add_argument('-f', '--force', dest='force', action='store_true', help='do not prompt')
rm_parser.add_argument('record', nargs='?', type=str, action='store', help='record path or UID')
rm_parser.error = raise_parse_exception
rm_parser.exit = suppress_exit


list_parser = argparse.ArgumentParser(prog='list|l', description='Display all record UID/titles')
list_parser.add_argument('pattern', nargs='?', type=str, action='store', help='search pattern')
list_parser.error = raise_parse_exception
list_parser.exit = suppress_exit


search_parser = argparse.ArgumentParser(prog='search|s', description='Search with regular expression')
search_parser.add_argument('pattern', nargs='?', type=str, action='store', help='search pattern')
search_parser.error = raise_parse_exception
search_parser.exit = suppress_exit


get_info_parser = argparse.ArgumentParser(prog='get|g', description='Display specified Keeper record/folder/team')
get_info_parser.add_argument('uid', type=str, action='store', help='UID')
get_info_parser.error = raise_parse_exception
get_info_parser.exit = suppress_exit


append_parser = argparse.ArgumentParser(prog='append-note|an', description='Append notes to existing record')
append_parser.add_argument('--notes', dest='notes', action='store', help='notes')
append_parser.add_argument('record', nargs='?', type=str, action='store', help='record path or UID')
append_parser.error = raise_parse_exception
append_parser.exit = suppress_exit


download_parser = argparse.ArgumentParser(prog='download-attachment', description='Download record attachments')
#download_parser.add_argument('--files', dest='files', action='store', help='file names comma separated. All files if omitted.')
download_parser.add_argument('record', nargs='?', type=str, action='store', help='record path or UID')
download_parser.error = raise_parse_exception
download_parser.exit = suppress_exit


class RecordAddCommand(Command):
    def get_parser(self):
        return add_parser

    def execute(self, params, **kwargs):
        title = kwargs['title'] if 'title' in kwargs else None
        login = kwargs['login'] if 'login' in kwargs else None
        password = kwargs['password'] if 'password' in kwargs else None
        url = kwargs['url'] if 'url' in kwargs else None
        custom_list = kwargs['custom'] if 'custom' in kwargs else None
        notes = kwargs['notes'] if 'notes' in kwargs else None

        generate = kwargs['generate'] if 'generate' in kwargs else None
        if generate:
            password = generator.generate(16)

        force = kwargs['force'] if 'force' in kwargs else None
        if not force:
            if not title:
                title = input('...' + 'Title: '.rjust(16))
            if not login:
                login = input('...' + 'Login: '.rjust(16))
            if not password:
                password = input('...' + 'Password: '.rjust(16))
            if not url:
                url = input('...' + 'Login URL: '.rjust(16))

        custom = []
        if custom_list:
            if type(custom_list) == str:
                pairs = custom_list.split(',')
                for pair in pairs:
                    idx = pair.find(':')
                    if idx > 0:
                        custom.append({
                            'name': pair[:idx].trim(),
                            'value': pair[idx+1:].trim()
                        })
            elif type(custom_list) == list:
                for c in custom_list:
                    if type(c) == dict:
                        name = c.get('name')
                        value = c.get('value')
                        if name and value:
                            custom.append({
                                'name': name,
                                'value': value
                            })

        folder = None
        folder_name = kwargs['folder'] if 'folder' in kwargs else None
        if folder_name:
            if folder_name in params.folder_cache:
                folder = params.folder_cache[folder_name]
            else:
                src = try_resolve_path(params, folder_name)
                if src is not None:
                    folder, name = src
        if folder is None:
            folder = params.folder_cache[params.current_folder] if params.current_folder else params.root_folder

        record_key = os.urandom(32)
        record_uid = api.generate_record_uid()
        rq = {
            'command': 'record_add',
            'record_uid': record_uid,
            'record_type': 'password',
            'record_key': api.encrypt_aes(record_key, params.data_key),
            'how_long_ago': 0
        }
        if folder.type in {BaseFolderNode.SharedFolderType, BaseFolderNode.SharedFolderFolderType}:
            rq['folder_uid'] = folder.uid
            rq['folder_type'] = 'shared_folder' if folder.type == BaseFolderNode.SharedFolderType else 'shared_folder_folder'

            sh_uid = folder.uid if folder.type == BaseFolderNode.SharedFolderType else folder.shared_folder_uid
            sf = params.shared_folder_cache[sh_uid]
            rq['folder_key'] = api.encrypt_aes(record_key, sf['shared_folder_key'])
            if 'key_type' not in sf:
                if 'teams' in sf:
                    for team in sf['teams']:
                        rq['team_uid'] = team['team_uid']
                        if team['manage_records']:
                            break
        else:
            rq['folder_type'] = 'user_folder'
            if folder.type != BaseFolderNode.RootFolderType:
                rq['folder_uid'] = folder.uid

        data = {
            'title': title or '',
            'secret1': login or '',
            'secret2': password or '',
            'link': url or '',
            'notes': notes or '',
            'custom': custom
        }
        rq['data'] =  api.encrypt_aes(json.dumps(data).encode('utf-8'), record_key)

        rs = api.communicate(params, rq)
        if rs['result'] == 'success':
            params.sync_data = True
            return record_uid
        else:
            print(rs['message'])


class RecordRemoveCommand(Command):
    def get_parser(self):
        return rm_parser

    def execute(self, params, **kwargs):
        folder = None
        name = None
        record_path = kwargs['record'] if 'record' in kwargs else None
        if record_path:
            rs = try_resolve_path(params, record_path)
            if rs is not None:
                folder, name = rs

        if folder is None or name is None:
            print('Enter name of existing record')
            return

        record_uid = None
        if name in params.record_cache:
            record_uid = name
            folders = list(find_folders(params, record_uid))
            #TODO support multiple folders
            if len(folders) > 0:
                folder = params.folder_cache[folders[0]] if len(folders[0]) > 0 else params.root_folder
        else:
            folder_uid = folder.uid or ''
            if folder_uid in params.subfolder_record_cache:
                for uid in params.subfolder_record_cache[folder_uid]:
                    r = api.get_record(params, uid)
                    if r.title.lower() == name.lower():
                        record_uid = uid
                        break

        if record_uid is None:
            print('Enter name of existing record')
            return

        del_obj = {
            'delete_resolution': 'unlink',
            'object_uid': record_uid,
            'object_type': 'record'
        }
        if folder.type in {BaseFolderNode.RootFolderType, BaseFolderNode.UserFolderType}:
            del_obj['from_type'] = 'user_folder'
            if folder.type == BaseFolderNode.UserFolderType:
                del_obj['from_uid'] = folder.uid
        else:
            del_obj['from_type'] = 'shared_folder_folder'
            del_obj['from_uid'] = folder.uid

        rq = {
            'command': 'pre_delete',
            'objects': [del_obj]
        }

        rs = api.communicate(params, rq)
        if rs['result'] == 'success':
            pdr = rs['pre_delete_response']

            force = kwargs['force'] if 'force' in kwargs else None
            np = 'y'
            if not force:
                summary = pdr['would_delete']['deletion_summary']
                for x in summary:
                    print(x)
                np = user_choice('Do you want to proceed with deletion?', 'yn', default='n')
            if np.lower() == 'y':
                rq = {
                    'command': 'delete',
                    'pre_delete_token': pdr['pre_delete_token']
                }
                rs = api.communicate(params, rq)
                if rs['result'] == 'success':
                    params.sync_data = True
                else:
                    print(rs['message'])


class SearchCommand(Command):
    def get_parser(self):
        return search_parser

    def execute(self, params, **kwargs):
        pattern = (kwargs['pattern'] if 'pattern' in kwargs else None) or ''

        # Search records
        results = api.search_records(params, pattern)
        if results:
            print('')
            display.formatted_records(results, params=params, skip_details=True)

        # Search shared folders
        results = api.search_shared_folders(params, pattern)
        if results:
            print('')
            display.formatted_shared_folders(results, params=params, skip_details=True)

        # Search teams
        results = api.search_teams(params, pattern)
        if results:
            print('')
            display.formatted_teams(results, params=params, skip_details=True)


class RecordListCommand(Command):
    def get_parser(self):
        return list_parser

    def execute(self, params, **kwargs):
        pattern = kwargs['pattern'] if 'pattern' in kwargs else None
        results = api.search_records(params, pattern or '')
        if results:
            display.formatted_records(results, params=params)


class RecordListSfCommand(Command):
    def execute(self, params, **kwargs):
        results = api.search_shared_folders(params, '')
        if results:
            display.formatted_shared_folders(results)


class RecordListTeamCommand(Command):
    def execute(self, params, **kwargs):
        results = api.search_teams(params, '')
        if results:
            display.formatted_teams(results)


class RecordGetUidCommand(Command):
    def get_parser(self):
        return get_info_parser

    def execute(self, params, **kwargs):
        uid = kwargs['uid'] if 'uid' in kwargs else None
        if not uid:
            print('UID parameter is required')
            return

        if api.is_shared_folder(params, uid):
            sf = api.get_shared_folder(params, uid)
            sf.display()
        elif api.is_team(params, uid):
            team = api.get_team(params, uid)
            team.display()
        elif uid in params.folder_cache:
            f = params.folder_cache[uid]
            f.display(params=params)
        else:
            api.get_record_shares(params, [uid])
            r = api.get_record(params, uid)
            if r:
                r.display(params=params)


class RecordAppendNotesCommand(Command):
    def get_parser(self):
        return append_parser

    def execute(self, params, **kwargs):
        name = kwargs['record'] if 'record' in kwargs else None

        if not name:
            self.get_parser().print_help()
            return

        record_uid = None
        if name in params.record_cache:
            record_uid = name
        else:
            rs = try_resolve_path(params, name)
            if rs is not None:
                folder, name = rs
                if folder is not None and name is not None:
                    folder_uid = folder.uid or ''
                    if folder_uid in params.subfolder_record_cache:
                        for uid in params.subfolder_record_cache[folder_uid]:
                            r = api.get_record(params, uid)
                            if r.title.lower() == name.lower():
                                record_uid = uid
                                break

        if record_uid is None:
            print('Enter name or uid of existing record')
            return

        notes = kwargs['notes'] if 'notes' in kwargs else None
        while not notes:
            notes = input("... Notes to append: ")

        record = api.get_record(params, record_uid)

        if record.notes:
            record.notes += '\n'
        record.notes += notes
        params.sync_data = True
        api.update_record(params, record)


class RecordDownloadAttachmentCommand(Command):
    def get_parser(self):
        return download_parser

    def execute(self, params, **kwargs):
        name = kwargs['record'] if 'record' in kwargs else None

        if not name:
            self.get_parser().print_help()
            return

        record_uid = None
        if name in params.record_cache:
            record_uid = name
        else:
            rs = try_resolve_path(params, name)
            if rs is not None:
                folder, name = rs
                if folder is not None and name is not None:
                    folder_uid = folder.uid or ''
                    if folder_uid in params.subfolder_record_cache:
                        for uid in params.subfolder_record_cache[folder_uid]:
                            r = api.get_record(params, uid)
                            if r.title.lower() == name.lower():
                                record_uid = uid
                                break

        if record_uid is None:
            print('Enter name or uid of existing record')
            return

        file_ids = []
        r = params.record_cache[record_uid]
        extra = json.loads(r['extra'].decode())
        if 'files' in extra:
            for f_info in extra['files']:
                file_ids.append(f_info['id'])

        if len(file_ids) == 0:
            print('No attachments associated with the record')
            return

        rq = {
            'command': 'request_download',
            'file_ids': file_ids,
        }
        api.resolve_record_access_path(params, record_uid, path=rq)

        rs = api.communicate(params, rq)
        if rs['result'] == 'success':
            for file_id, dl in zip(file_ids, rs['downloads']):
                if 'url' in dl:
                    file_key = None
                    file_name = None
                    extra = json.loads(r['extra'].decode())
                    if 'files' in extra:
                        for f_info in extra['files']:
                            if f_info['id'] == file_id:
                                file_key = base64.urlsafe_b64decode(f_info['key'] + '==')
                                file_name = f_info['name']
                                break

                    if file_key:
                        rq_http = requests.get(dl['url'], stream=True)
                        with open(file_name, 'wb') as f:
                            print('Downloading \'{0}\''.format(os.path.abspath(f.name)))
                            iv = rq_http.raw.read(16)
                            cipher = AES.new(file_key, AES.MODE_CBC, iv)
                            finished = False
                            while not finished:
                                to_decrypt = rq_http.raw.read(10240)
                                if len(to_decrypt) > 0:
                                    decrypted = cipher.decrypt(to_decrypt)
                                    f.write(decrypted)
                                else:
                                    finished = True
                    else:
                        print('File \'{0}\': Failed to file encryption key'.format(file_name))
                else:
                    print('File \'{0}\' download error: {1}'.format(file_id, dl['message']))

