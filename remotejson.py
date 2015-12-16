#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import paramiko


class RemoteJson():
    """
        Class purpose is to help to read or modfy a remote json
    """

    def __init__(self, host, username, path, password=None, key=None):
        """
            Args:
                host (str): hostname where to connect
                username (str): username of the mahcine
                password (str): password of the machine
                path (str): Json path
                key (str): Path to RSA pub key if used
                password will be by-passed
        """
        self.host = host
        self.username = username
        self.password = password
        self.path = path
        self.key = key

    def _get_handle(self):
        """ Provide an paramiko transport object to be used
            Returns:
                transport (obj): Paramiko Transport object
        """

        # Setup transport
        transport = paramiko.Transport((self.host, 22))

        if self.key is not None:
            private_key = paramiko.RSAKey.from_private_key_file(self.key)
            transport.connect(username=self.username, pkey=private_key)
        else:
            transport.connect(username=self.username, password=self.password)

        # Setup SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)

        return transport

    def value(self):
        """
            Return The JSON File
        """

        transport = self._get_handle()
        # Open a json and returns the value
        with transport.open_sftp_client().file(self.path) as sftp_file:
            return json.loads(sftp_file.read().decode('utf-8'))

    def set(self, section, element, new_value):
        """ Put new element change value of an old element
        Args:
            section (str): Section where changes must be done
            element (str): Element to put or change
            new_value (str): new value of the element or changed element
        """
        # Setup transport
        transport = self._get_handle()

        with transport.open_sftp_client().file(
                self.path, mode='r', bufsize=-1) as json_file:

            data = json.load(json_file)

            # elect a section
            section_data = data[section]

            # Select the element and update a value
            section_data[element] = new_value

            with transport.open_sftp_client().file(
                    self.path, mode='w', bufsize=-1) as json_file:
                json_file.write(json.dumps(data, sort_keys=True, indent=4))

    def append(self, section, dictionnary):
        """ Append a new section in the json file
            Args :
                section (str): section to be added
                dictionnary (dict) : data to be added in a dict fashion
        """

        # Setup transport
        transport = self._get_handle()

        # Read json_file
        with transport.open_sftp_client().file(
                self.path, mode='r', bufsize=-1) as json_file:

            # Load the json_file
            data = json.load(json_file)

            # Update Json
            data[section] = dictionnary

            with transport.open_sftp_client().file(
                    self.path, mode='w', bufsize=-1) as json_file:

                json_file.write(json.dumps(data))

    def delete_section(self, section):
        """Delete a section in jsonfle
            param :
                section (str): section to be deleted

        """

        # Setup transport
        transport = self._get_handle()

        # Read json_file
        with transport.open_sftp_client().file(
                self.path, mode='r', bufsize=-1) as json_file:

            # Load the json_file
            data = json.load(json_file)

            del data[section]
            # Update Json

            print data
            with transport.open_sftp_client().file(
                    self.path, mode='w', bufsize=-1) as json_file:
                json_file.write(json.dumps(data))

    def delete_element(self, section, element):
        """Delete a particular element in the section
            Args:
                section: section to be added
                element : python dictionnary
        """

        # Setup transport
        transport = self._get_handle()

        with transport.open_sftp_client().file(
                self.path, mode='r', bufsize=-1) as json_file:

            data = json.load(json_file)

            # Select a section
            section_data = data[section]

            # Select the element and update a value
            del section_data[element]

            with transport.open_sftp_client().file(
                    self.path, mode='w', bufsize=-1) as json_file:
                json_file.write(json.dumps(data))
