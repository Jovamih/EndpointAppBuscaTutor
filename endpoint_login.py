import pymysql
import sys
import json



host="buscatutordatabase.cuxsffuy95k9.us-east-1.rds.amazonaws.com"
port=3306
user="admin"
password="admin12345678"
db="buscatutor"


def lambda_handler(event, context):
  
    params=event["queryStringParameters"]
    correo=params["correo"]
    passwd=params['password']
    content=None
    #todo implement
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        query=f"SELECT * FROM Estudiante WHERE correo='{correo}' AND password='{passwd}';"
        cursor.execute(query)
        result=cursor.fetchone()

    if not result:
        content={'success':False,"data":None}
    else:
        es_tutor= result[5]==1 #si tutor es 1, devolvemos true, en caso contrario False
        content={"success":True,"data":{
            'id_estudiante':result[0],
            'correo':result[1],
            'password':result[2],
            'nombre_completo':result[3],
            'num_telefono':result[4],
            'es_tutor': es_tutor
        }}
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(content)
    }


    