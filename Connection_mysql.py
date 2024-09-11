# pip install mysql-connector-python
import mysql.connector as  mycon


def mysql_connection(myid, mypw):

    try:
        connection = mycon.connect(
            host='192.168.3.4',
            port=3306,
            user=myid,
            password=mypw,
            database='analyze_db',
            ssl_ca=r'C:\Program Files\OpenSSL-Win64\ssl\ca.pem',
            ssl_cert=r'C:\Program Files\OpenSSL-Win64\ssl\client-cert.pem',
            ssl_key=r'C:\Program Files\OpenSSL-Win64\ssl\client-key.pem'
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW STATUS LIKE 'Ssl_cipher';")
        result = cursor.fetchone()
        
        if result and result[1]:
            print(f"SSL is enabled. Cipher = {result[1]}")
        else:
            print("SSL is not enabled")
        
    except mycon.Error as err:
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mycon.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)




if __name__ == "__main__":
    id = 'pcb'
    pw = '1403'
    
    mysql_connection(id, pw)
    
    