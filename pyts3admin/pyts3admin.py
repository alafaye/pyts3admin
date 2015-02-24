import pyts3


def check_command_status(status):

    if status == 'error id=0 msg=ok':
        return 0
    else:
        return 1


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


class ClientList(object):

    def __init__(self):
        raise NotImplementedError


class Channel(object):

    def __init__(self):
        raise NotImplementedError


class ChannelList(Channel):

    def __init__(self):
        raise NotImplementedError


class AdminSession(object):

    def __init__(self, verbosity=0, ip='localhost', port='10011',
                 admin_login='serveradmin', password=None):

        self.admin_login = admin_login
        self.ip = ip
        self.port = port

        ts = pyts3.PyTS3.ServerQuery(ip=ip, query=port)

        ts.connect()
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

        return self.ts.command('banadd', params)

    def ban_client(self, client_id=None, time=3600, reason='For reasons'):
        r"""
        Method to ban clients

        Parameters
        ----------
        client_id : int
        time : int
        reason : string
        """
        params = {'clid': str(client_id), 'time': str(time), 'banreason': reason}
        return self.ts.command('banclient', params)

    # Chan part

    def channel_create(self, chan_name=None, **kwargs):
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
        return self.ts.command('channelcreate', params)

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

        params = {'channel_name': chan_name, 'force': force}
        return self.ts.command('channeldelete', params)

    def channel_edit(self, channel_id, **kwargs):

        params = {'cid': channel_id}
        params.update(kwargs)
        return self.ts.command('channeledit', kwargs)

    def channel_move(self, channel_id, parent_channel_id, order=0):

        params = {'cid': channel_id, 'cpid': parent_channel_id, 'order': order}
        return self.ts.command('channelmove', params)

    def channel_find(self, pattern):

        return self.ts.command('channelfind', pattern=pattern)

    def choose_virtual_server(self, server_id):
        raise NotImplementedError

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

        return self.ts.command('clientmove', params)

    def client_edit(self, client_id, **kwargs):

        params = {'clid': client_id}
        params.update(kwargs)
        return self.ts.command('clientedit', params)

    def client_find(self, pattern):
        return self.ts.command('clientfind', {'pattern': pattern})

    def client_get_ids(self, client_uid):
        return self.ts.command('clientgetids', {'cluid': client_uid})

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

    def client_db_list(self):
        return self.ts.command('clientdblist')

    def client_perm_list(self, client_dbid):
        raise NotImplementedError

    def client_kick(self, clients_id, from_server=False,
                    reason='For reasons'):

        kickout = 4
        if from_server:
            kickout = 5

        if not isinstance(clients_id, int):
            for client in clients_id:
                clients_id = str(client) + '|'

        params = {'reasonid': str(kickout), 'reasonmsg': str(reason),
                  'clid': str(clients_id)}

        return self.ts.command('clientkick', params)

    def client_poke(self, client_id, msg):
        raise NotImplementedError

    def server_list(self):
        serverlist = self.ts.command('serverlist')
        return serverlist

    def virtual_server_ids(self):

        ids = []
        for server in self.server_list():
            ids.append(server['virtualserver_id'])

        return ids

    def snapshot_create():
        raise NotImplementedError

    def snapshot_deploy():
        raise NotImplementedError

    def general_message(self, msg):
        return self.ts.command('gm', msg=msg)
