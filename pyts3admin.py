import pyts3


class Client(object):

    def __init__(self, ts, name=None, clid=None, dbid=None, cluid=None):

        self.ts = ts
        if name:
            self.name = name
        if clid:
            self.clid = clid
        if dbid:
            self.dbid = dbid
        if cluid:
            self.cluid = cluid


class AdminSession(object):
    r"""
    Defines an admin session on the target server

    Parameters
    ----------
    verbosity : int
        verbosity of the output 0 for low, 1 for high
    ip : string
        ip of target server, can also be an hostname
    port : int
        port of the target server to query
    admin_login : string
        login username of an server admin
    password : string
        password of the admin user

    """

    def __init__(self, verbosity=0, ip='localhost', port=10011,
                 admin_login='serveradmin', password=None):

        self.admin_login = admin_login
        self.ip = ip
        self.port = str(port)

        ts = pyts3.PyTS3.ServerQuery(ip=ip, query=port)

        if ts.connect():
            print("Connected to the server")
        else:
            raise RuntimeError("Failed to connect to the server!")

        print(ts.command('login {} {}'.format(admin_login, password)))

        # if not ts.command('login {} {}'.format(admin_login, password)):
        #     raise RuntimeError("Admin login failed")

        self.ts = ts

    def __del__(self):
        if self.ts.connect():
            self.ts.disconnect()

    # Ban part

    def ban_list(self):
        r"""
        Returns the ban list of the choosen server

        Returns
        -------
        out : list of dictionnaries
            The dictionnary fields are:
                bannid : int
                created : int
                duration : int
                enforcements : int
                invokercldbid : int
                invokername : unicode
                invokeruid : unicode
                name : unicode
                reason : unicode

        """
        return self.ts.command('banlist')

    def ban_add_rule(self, ip=None, name=None, client_UID=None,
                     reason='For reasons', time=600):
        r"""
        Method to add rules to ban clients

        Parameters
        ----------
        ip : string
            regex matching the ip's to ban
        name : string
            regex matching the usernames to ban
        client_UID : int
        reason : string
        time : int
            in seconds default=10minutes

        Notes
        -----
        There should be at lest one of those:
        ip, name, client_UID
        You can only add a rule type at a time, e.g. only ip or only name.
        If multiple definitions, this is the order in wich it will be taken
        into account:
        name -> ip -> client_UID

        """
        client_UIDstr = str(client_UID)
        time = str(time)

        if name is not None:
            params = {'name': name}
        elif ip is not None:
            params = {'ip': ip}
        elif client_UID is not None:
            params = {'clid': client_UIDstr}
        else:
            raise RuntimeError("Please input at least ip or name or \
                               client_UID")

        params.update({'banreason': reason, 'time': time})

        return self.ts.command('banadd', **params)

    def ban_client(self, client_id=None, time=3600, reason='For reasons'):
        r"""
        Method to ban clients

        Parameters
        ----------
        client_id : int
        time : int
        reason : string

        """
        params = {'clid': str(client_id), 'time': str(time),
                  'banreason': reason}
        return self.ts.command('banclient', **params)

    # Chan part

    def channel_create(self, chan_name=None, permanent=False, **kwargs):
        r"""
        Method to create channels

        Parameters
        ----------
        chan_name : string

        """

        if chan_name is None:
            raise RuntimeError('You have to define a target chan to create')

        params = {'channel_name': chan_name}
        params.update(kwargs)
        if permanent:
            params.update({'channel_flag_permanent': 1})
        return self.ts.command('channelcreate', **params)

    def channel_delete(self, chan_name, force=False):
        r"""
        Method to delete channels

        Parameters
        ----------
        chan_name : string
        force : bool

        """

        if force:
            force = 1
        else:
            force = 0

        params = {'cid': chan_name, 'force': force}
        print(params)
        return self.ts.command('channeldelete', **params)

    def channel_edit(self, channel_id, **kwargs):
        r"""
        To edit channel designed by the channel id

        Parameters
        ----------
        channel_id : int
            target channel id
        kwargs : dict
            fields to edit
        """

        params = {'cid': str(channel_id)}
        params.update(kwargs)
        return self.ts.command('channeledit', kwargs)

    def channel_list(self, *args):
        r"""
        Output a list of channels from the server

        Parameters
        ----------
        *args : topic
                flags
                voice
                limits
                icon
                secondsempty
            All those must be passed as strings
            e.g. : ts.client_list('topic', 'flags')
        """

        return self.ts.command('channellist', *args)

    def channel_move(self, channel_id, parent_channel_id, order=0):
        r"""
        Moves a channel under another

        Parameters
        ----------
        channel_id : int
        parent_channel_id : int
        order : int
            Indicates the new position under the parent channel
            e.g. 0=first, 1=second etc...

        """

        params = {'cid': str(channel_id), 'cpid': str(parent_channel_id), 'order': order}
        return self.ts.command('channelmove', **params)

    def channel_find(self, pattern):
        r"""
        Find a channel following a name pattern

        Parameter
        ---------
        pattern : string
        """

        return self.ts.command('channelfind', pattern=pattern)

    def choose_virtual_server(self, server_id):
        r"""
        To choose a virtual server

        Parameter
        ---------
        server_id : int
        """

        cmd = 'use ' + str(server_id)
        return self.ts.command(cmd)

    def stop_server(self):
        raise NotImplementedError

    # client part

    def client_move(self, target_channel_id, clients_id,
                    channel_password=None):
        r"""
        Method to move one or more clients to another chan

        Parameters
        ----------
        target_channel : int
        clients_id : int or list
        channel_password : string

        """

        if not isinstance(clients_id, int):
            for client in clients_id:
                clients_id = str(client) + '|'

        params = {'cid': target_channel_id, 'clid': str(clients_id)}
        if channel_password is not None:
            params.update('cpw', channel_password)

        return self.ts.command('clientmove', **params)

    def client_edit(self, client_id, **kwargs):
        r"""
        To edit a client properties

        Parameters
        ----------
        client_id : int
        kwargs : dict
        """

        params = {'clid': str(client_id)}
        params.update(kwargs)
        return self.ts.command('clientedit', **params)

    def client_find(self, pattern):
        r"""
        Find a client following a name pattern

        Parameter
        ---------
        pattern : string
        """
        return self.ts.command('clientfind', {'pattern': pattern})

    def client_dblist(self):
        r"""
        Lists clients registered in the ts3 database

        Returns:
        out : list of dicts
            dict fields :
                cldbid : int
                client_created : int
                client_lastconnected : int
                client_lastip : unicode
                client_nickane : unicode
                client_totalconnections : int
                client_unique_identifier : unicode
        """
        return self.ts.command('clientdblist')

    def client_get_ids(self, client_uid):
        return self.ts.command('clientgetids', **{'cluid': client_uid})

    def client_list(self, *args):
        r"""
        Returns a list of clients online on a virtual server.

        Parameters
        ----------
        args :  uid
                away
                voice
                times
                groups
                info
                country
                ip
            All those must be passed as strings
            e.g. : ts.client_list('uid', 'ip')

        """
        return self.ts.command('clientlist', *args)

    def client_perm_list(self, client_dbid):
        raise NotImplementedError

    def client_kick(self, clients_id, from_server=False,
                    reason='For reasons'):
        r"""
        To kick one or more clients from a channel or from the server

        Parameters
        ----------
        clients_id : list or int
        from_server : bool
            To indicate wether the client should be kicked for the server
        reason : string
            Reason of the kick displayed to the client
        """

        kickout = 4
        if from_server:
            kickout = 5

        if not isinstance(clients_id, int):
            for client in clients_id:
                clients_id = str(client) + '|'

        params = {'reasonid': str(kickout), 'reasonmsg': str(reason),
                  'clid': str(clients_id)}

        return self.ts.command('clientkick', **params)

    def client_poke(self, client_id, msg):
        raise NotImplementedError

    def server_list(self):
        """
        Returns a list of the available virtual servers

        Returns
        -------
        out : list of dicts
            dict fields :
                virtualserver_autostart : int
                virtualserver_clientsonline : int
                virtualserver_id : int
                virtualserver_maxclients : int
                virtualserver_name : unicode
                virtualserver_port : int
                virtualserver_queryclientsonline : int
                virtualserver_status : unicode
                virtualserver_uptime : int
        """

        return self.ts.command('serverlist')

    def virtual_server_ids(self):
        r"""
        Returns a list if the virtualserver ids

        Returns
        -------
        out : list
        """

        ids = []
        for server in self.server_list():
            ids.append(server['virtualserver_id'])

        return ids

    def snapshot_create():
        raise NotImplementedError

    def snapshot_deploy():
        raise NotImplementedError

    def general_message(self, msg):
        r"""
        To send a mesage to the ts3 general chat

        Parameters
        ----------
        msg : string
            Message to send
        """
        return self.ts.command('gm', msg=msg)
