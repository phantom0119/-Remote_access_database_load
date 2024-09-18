# pip install mysql-connector-python
import mysql.connector as  mycon
from date_dim_dataset import dataset


def mysql_connection(myid, mypw):

    try:
        connection = mycon.connect(
            host='192.168.3.4',
            port=3306,
            user=myid,
            password=mypw,
            database='analyze_db',
            ssl_ca=r'C:\Program Files\OpenSSL-Win64\ssl\ca.pem',            # 인증기관 Key
            ssl_cert=r'C:\Program Files\OpenSSL-Win64\ssl\client-cert.pem', # 클라이언트 인증서
            ssl_key=r'C:\Program Files\OpenSSL-Win64\ssl\client-key.pem'    # 클라이언트 Key
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW STATUS LIKE 'Ssl_cipher';")
        
        # 결과에서 첫 번째 행만 튜플로 추출.
        result = cursor.fetchone()
        # 전체 결과 = cursor.fetchall()
        
        # SSL 활성화 상태면 암호화 알고리츰을 출력함.
        if result and result[1]:
            print(f"SSL is enabled. Cipher = {result[1]}")
            return connection, cursor
        else:
            print("SSL is not enabled")
            return None, None
        
    except mycon.Error as err:
            # 계정 접속 오류
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            # DB 연결 오류
        elif err.errno == mycon.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None, None
        


# 실습용 데이터 적재 샘플 획득 
def set_insert_data():
    data = dataset 
    print(f"The number of rows : {len(dataset)}")
    return data
    
    
# CREATE TABLE
def mysql_create_table_practice(connection, cursor):
    create_sql = """
        CREATE TABLE IF NOT EXISTS date_dim
        (
            date                 date,
            date_key             integer,
            day_of_month         integer,
            day_of_year          integer,
            day_of_week          integer,
            day_name             text,
            day_short_name       text,
            week_number          integer,
            week_of_month        integer,
            week                 date,
            month_number         integer,
            month_name           text,
            month_short_name     text,
            first_day_of_month   date,
            last_day_of_month    date,
            quarter_number       integer,
            quarter_name         text,
            first_day_of_quarter date,
            last_day_of_quarter  date,
            year                 integer,
            decade               integer,
            centurys             integer
        );
    """
    try:
        if cursor:  # 커서 객체가 있다면
            cursor.execute(create_sql)
        
        print("CREATE TABLE 'date_dim'.")
    except mycon.Error as err:
        print(f"CREATE TABLE ERROR : \n{err}")
        
    

# INSERT DATASET
def mysql_insert_table_practice(connection, cursor, indata):
    
    
    

if __name__ == "__main__":
    id = 'pcb'
    pw = '1403'
    
    connection, cursor = mysql_connection(id, pw)   # Mysql연결 객체와 커서 객체 획득
    indata = set_insert_data()
    mysql_create_table_practice(connection, cursor)
    mysql_insert_table_practice(connection, cursor, indata)
    
    
    