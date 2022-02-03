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
    id=params["id"]
    content=None
    #todo implement
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        query=f"SELECT * FROM Estudiante WHERE id_estudiante={id};"
        cursor.execute(query)
        result=cursor.fetchone()

    if not result:
        content={'success':False,"data":None}
    else:
        
        content={"success":True,"data":{
                                        'id_estudiante':result[0],
                                        'correo':result[1],
                                        'password':result[2],
                                        'nombre_completo':result[3],
                                        'num_telefono':result[4],
                                        'es_tutor': result[5]==1
        }}
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(content)
    }


    