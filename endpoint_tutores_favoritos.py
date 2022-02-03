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
    id=int(params["id"])
    
    tutores_favoritos=list()
    #todo implement
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        query=f"""SELECT T.id_tutor, E.nombre_completo,T.descripcion, T.foto FROM Tutor as T
                	    LEFT JOIN Estudiante as E ON T.id_estudiante=E.id_estudiante
                        WHERE T.id_tutor IN (
                						SELECT id_tutor FROM Favoritos
                						WHERE id_estudiante={id}
                );"""
        cursor.execute(query)
        result=cursor.fetchall()
        
    #iteramos sobre el resultado de tutores
    for row in result:
        tutores_favoritos.append({
            "id_tutor":row[0],
            "nombre_completo":row[1],
            "descripcion":row[2],
            "foto":row[3]
        })
        
    
    return {
        'statusCode': 200,
        'body': json.dumps({"id_estudiante":int(id),"tutores_favoritos":tutores_favoritos})
    }

