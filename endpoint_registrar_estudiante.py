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
    correo=params['correo']
    passd=params['password']
    nombre_completo=params['nombre_completo']
    num_telefono=params['num_telefono']
    es_tutor=int(params['es_tutor'])
    
    #definimos la estructura de las consultas
    
    query_registrar="""INSERT INTO Estudiante(correo,password,nombre_completo,num_telefono,es_tutor)
    
                        VALUES(%s,%s,%s,%s,%s);
                        """
    


    #definimos la consulta para obtener el ultimo ID
    query_lastID="SELECT MAX(id_estudiante) FROM Estudiante;"
    
    
    query_exist_mail="SELECT correo FROM Estudiante WHERE correo=%s;"
    
    

    content=None
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        
        cursor.execute(query_exist_mail,(correo,))
        
        row=cursor.fetchone()
        
          
            #si el correo ya existe
        if row:
             content= {
                        "status":3,
                        "message":"El correo ya existe en la base de datos. No se inicia registro."
                    }
            
            
        else:
           
            #si no existen correos identicos procedemos a registrar al estudiante
            
        
            #inicio del registro
            cursor.execute(query_registrar,(correo,passd,nombre_completo,num_telefono,es_tutor))
            
            conn.commit()
            if cursor.rowcount>0:
                
                cursor.execute(query_lastID)
                result=cursor.fetchone()
                
                content= {
                        "status":1,
                        "message":"Insercion exitosa en la base de datos",
                        "id_estudiante":int(result[0])
                    }
            else:
                content= {
                        "status":2,
                        "message":"Error de insercion en la base de datos."
                    }

    return {
        "statusCode":200,
        "body":json.dumps(content)
        
        }
