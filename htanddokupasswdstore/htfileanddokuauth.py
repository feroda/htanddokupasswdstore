from trac.core import *
from trac.config import Option
from acct_mgr.util import EnvRelativePathOption

from acct_mgr.api import IPasswordStore
from acct_mgr.htfile import HtPasswdStore

import crypt


class HtFileAndDokuAuthStore(HtPasswdStore):
    """
    A password backend for AccountManager that uses:

    * htpasswd files and if not found
    * dokuwiki passwd files

    """
    implements(IPasswordStore)

    dokupasswd_path = Option(
        'account-manager', 'dokupasswd_file',
        default='/var/www/doku/conf/users.auth.php',
        doc='Path to the users.auth.php dokuwiki file')

    def config_key(self):
        raise NotImplementedError("ciao")

    def set_password(self, *args, **kw):
        raise NotImplementedError("Cannot update passwords via the web ui")

    def delete_user(self, *args, **kw):
        raise NotImplementedError("Cannot update passwords via the web ui")

    def _get_users(self, filename):
        """
        Return all users in the htpasswd file and then
        all users in the dokupasswd file
        """
        try:
            super(HtFileAndDokuAuthStore, self)._get_users(filename)
        except StopIteration:
            pass
        try:
            with open(self.dokupasswd_path, 'rU') as f:
                for line in f:
                    if line and not line.startswith('#'):
                        user = line.split(':', 1)[0]
                        if user:
                            yield user.decode('utf-8')
        except IOError:
            self.log.error(
                'acct_mgr: _get_users() -- '
                'Can\'t read doku password file "%s"' % filename)

    def _check_dokuuserline(self, user, password, hashed):
        self.log.info('user=%s passwd=%s, hashed=%s, rv=%s' % (user, password, hashed,crypt.crypt(password, '$1$') == hashed))
        return crypt.crypt(password, '$1$') == hashed

    def check_password(self, user, password):
        """
        Check users against the htpasswd file and then the users.auth.php doku file
        """
        rv = super(HtFileAndDokuAuthStore, self).check_password(user, password)
        if rv is None:
            user = user.encode('utf-8')
            password = password.encode('utf-8')
            prefix = self.prefix(user)
            l = len(prefix)
            filename = self.dokupasswd_path
            try:
                with open(filename, 'rU') as f:
                    for line in f:
                        if line.startswith(prefix):
                            return self._check_dokuuserline(
                                user, password,
                                line[l:line.find(':', l)])
            except IOError:
                self.log.error(
                    'acct_mgr: check_password() -- '
                    'Can\'t read doku password file "%s"' % filename)

        return rv
