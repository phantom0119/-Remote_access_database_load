# pip install mysql-connector-python
import mysql.connector as  mycon

def mysql_connection(myid, mypw):
    connection = mycon.connect(
        host='192.168.3.4',
        user=myid,
        password=mypw
    )




if __name__ == "__main__":
    id = 'pcb'
    pw = '1403'
    
    