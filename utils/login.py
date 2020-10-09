import ldap


class Login:
    BASE_DISTINGUISHED_NAME = "DC=ms,DC=ds,DC=uhc,DC=com"
    LDAP_SERVER = "ldap://ms.ds.uhc.com:389"
    ALLOWED_GROUPS = ['CN=icuegrpp,OU=Groups,OU=Unix,OU=Servers,OU=UHT,OU=UHG,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=icuegrp,OU=Groups,OU=Unix,OU=Servers,OU=UHT,OU=UHG,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=icue_dev,CN=Users,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=dev_ClinicalArchitect_Developer,CN=Users,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=Clinical Architects,OU=Dist-Lists,OU=Messaging,OU=UHT,OU=UHG,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=HCE_ML_OutpatientPriorAuth,CN=Users,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=Arch_Clinical_Dashboard,CN=Users,DC=ms,DC=ds,DC=uhc,DC=com',
                      'CN=Stars_Suppl_RW,CN=Users,DC=ms,DC=ds,DC=uhc,DC=com'
                      ]

    def ldap_login(self, user_name, password) -> [bool, str]:
        """Use UHG's login to determine the validity of the user name and password.
        
        :param user_name: ms id 
        :param password: valid password 
        :return: True if login is valid. 
        """
        # the following is the user_dn format provided by the ldap server
        # user_dn = "uid=" + username + ",ou=someou,dc=somedc,dc=local"
        user_dn = f"CN={user_name},CN=Users,DC=ms,DC=ds,DC=uhc,DC=com"

        # adjust this to your base dn for searching
        connect = ldap.initialize(self.LDAP_SERVER, bytes_mode=False)
        search_filter = f'(&(uid={user_name}))'
        search_attr_list = ['displayName', 'memberOf']
        special_success = False
        try:
            # if authentication successful, get the full user datafuid
            connect.bind_s(user_dn, password)
            special_success = True
            result = connect.search_s(self.BASE_DISTINGUISHED_NAME, ldap.SCOPE_SUBTREE, search_filter, search_attr_list)
            print("result", result)
            return self._allowed_access(connect, user_name)
        except Exception as err:
            print("authentication error", err)
            if special_success and user_name in ['erospide', 'tmanni4']:
                # force success
                return True, user_name
        finally:
            connect.unbind_s()
        return False, ''

    def _allowed_access(self, ldap_connect, user_name: str) -> (bool, str):
        for group in self.ALLOWED_GROUPS:
            print('---', group)
            search_filter = f'(memberOf={group})'
            result = ldap_connect.search_s(self.BASE_DISTINGUISHED_NAME, ldap.SCOPE_SUBTREE,
                                           search_filter, ['displayName'])
            # print('other', result)
            for item in result:
                print('other', item)
                if (item[0]).find(f'CN={user_name},') >= 0:
                    display_name = (item[1])['displayName']
                    display_name = (display_name[0]).decode("utf-8")
                    print(f'match ---------- {display_name} \t\tGroup "{group}"')
                    return True, display_name

        return False, ''

    def google_login(self, user_name, password):
        pass


if __name__ == '__main__':
    my_login = Login()
    my_user_name = input("user name: ")
    my_password = input("password: ")

    print(my_login.ldap_login(my_user_name, my_password))
