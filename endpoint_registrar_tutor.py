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
    id_estudiante=params['id_estudiante']
    descripcion=params['descripcion']
    foto=params['foto']
    habilidades=params['habilidades']
    especialidades=params['especialidades']
    
    #especialidades separadas
    habilidades=habilidades.split(",")
    especialidades=especialidades.split(",")
    

    
    #Verificamos si existe un estudiante ya registrado como tutor
    query_estud="SELECT * FROM Tutor WHERE id_estudiante=%s;"
    
    #definimos la estructura de las consultas
    
    query_registrar="""INSERT INTO Tutor(id_estudiante,descripcion,foto)
    
                        VALUES(%s,%s,%s);
                        """
    #definimos la consulta para obtener el ultimo ID
    query_lastID="SELECT MAX(id_tutor) FROM Tutor;"
    
    
    #query insert habilidades
    query_habilidades="INSERT INTO HabilidadesTutor(id_tutor,desc_habilidad) VALUES (%s,%s)"
    #query insert especialidad
    query_especialidad="INSERT INTO EspecialidadesTutor(id_tutor,desc_especialidad) VALUES(%s,%s)"
    

    content=None
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        
        cursor.execute(query_estud,(id_estudiante,))
        result=cursor.fetchone()
        
        #si ya existe un estudiante registrado como tutor
        if result:
            content={
                "success":False,
                "message":"El usuario ya estaba registrado como tutor. Registre otro.",
                "id_tutor":None
            }
        else:
            
            try:
                #obtenemos el ID del ultimo registro de tutor agregado
                cursor.execute(query_lastID)
                result=cursor.fetchone()
                id_tutor=int(result[0])+1 if result[0] else 1 # el id de tutor esta generado
                #ejecutamos na insercion en el registro
                cursor.execute(query_registrar,(id_estudiante,descripcion,foto))
                
                #REGISTRAMOS LAS HABILIDADES DEL TUTOR
                lst_habilidades=[(id_tutor,habilidad) for habilidad in habilidades]
                
                #insertamos la habilidades
                cursor.executemany(query_habilidades,lst_habilidades)
                    
          
                #REGISTRAMOS LAS ESPECIALIDADES
                lst_especialidades=[(id_tutor,especialidad) for especialidad in especialidades]
                cursor.executemany(query_especialidad,lst_especialidades)
                
                #Actualizamos el estado tutor del estudiante
                cursor.execute("UPDATE Estudiante SET es_tutor=1 WHERE id_estudiante=%s",(id_estudiante,))
                
                #confirmamos todos los cambios
                conn.commit()
                
                conn.close()
                    
                content={
                    "success":True,
                    "message":"Registro exitoso de Tutor",
                    "id_tutor":id_tutor
                }
            except Exception as e:
                conn.rollback()
                conn.close()
            
                content={
                    "success":False,
                    "message":"Registro fallido de Tutor",
                    "id_tutor":None
                }
            
            

    return {
        "statusCode":200,
        "body":json.dumps(content)
        
        }
