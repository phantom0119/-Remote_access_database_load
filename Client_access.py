import Connection_ssh as sshc



if __name__ == "__main__" :
    svpw = sshc.get_ssh_password()
    svinfo = sshc.get_ssh_info()
    
    status, MysqlId, MysqlPw = sshc.connect_ssh(svinfo['IP'], 
                                        svinfo['PORT'], 
                                        svinfo['ID'], 
                                        svpw)
    
    print(status, MysqlId, MysqlPw)
    