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
    
    #definimos la estructura de las consultas
    
    if "id" in params.keys():
        id=params['id']
        query_info=f"""SELECT T.id_tutor, E.nombre_completo, E.num_telefono, T.descripcion,T.foto FROM Tutor as T
                    	LEFT JOIN Estudiante as E ON T.id_estudiante=E.id_estudiante
                        WHERE T.id_tutor={id}
             ;"""
    elif "select" in params.keys():
        
        limit=int(params['select'])
        
        if limit<0: #si el query es negativo -1 devolvemos todos los registros
             query_info=f"""SELECT T.id_tutor, E.nombre_completo, E.num_telefono,T.descripcion, T.foto FROM Tutor as T
                	LEFT JOIN Estudiante as E ON T.id_estudiante=E.id_estudiante
              ;"""
        else:
            query_info=f"""SELECT T.id_tutor, E.nombre_completo, E.num_telefono,T.descripcion, T.foto FROM Tutor as T
                    	LEFT JOIN Estudiante as E ON T.id_estudiante=E.id_estudiante
                        LIMIT {limit}
             ;"""
    elif "especialidad" in params.keys():
        especialidad=params['especialidad']
        query_info=f"""
                    SELECT T.id_tutor, E.nombre_completo, E.num_telefono,T.descripcion,T.foto FROM Tutor as T
                        	LEFT JOIN Estudiante as E ON T.id_estudiante=E.id_estudiante
                            LEFT JOIN EspecialidadesTutor as ET ON T.id_tutor=ET.id_tutor
                    WHERE ET.desc_especialidad LIKE '%{especialidad}%';
        
                    """
    else:
        return { 'statusCode': 200,
                'body': json.dumps({"mensaje":"Los parametros enviados son incorrectos. Use id o select"})
                }
       
    #consulta de especialidades de los tutores
    query_especialidades="""SELECT ET.desc_especialidad FROM Tutor as T LEFT JOIN EspecialidadesTutor as ET ON T.id_tutor= ET.id_tutor WHERE T.id_tutor= %s;""" 	    
        
    #consulta de las habilidades de los tutores
    query_habilidades="""SELECT HT.desc_habilidad FROM Tutor as T LEFT JOIN HabilidadesTutor as HT ON T.id_tutor= HT.id_tutor WHERE T.id_tutor= %s;"""  
            
    
    lista_tutores=list()
    #todo implement
    conn=pymysql.connect(host=host,user=user,password=password,db=db,connect_timeout=5)
    with conn.cursor() as cursor:
        cursor.execute(query_info)
        result=cursor.fetchall()
        
        #primero consultamos al tutor
        for row in result:
            content={
                "id_tutor":row[0],
                "nombre_completo":row[1],
                "num_telefono":row[2],
                "descripcion":row[3],
                "foto":row[4],
                "especialidades":[],
                "habilidades":[]
            }
            id_tutor=row[0]
            #consultamos las espececialidades del tutor
            cursor.execute(query_especialidades,(id_tutor,))
            result_especialidades=cursor.fetchall()
            for row_esp in result_especialidades:
                if row_esp[0]:
                    content["especialidades"].append(row_esp[0])
                
            cursor.execute(query_habilidades,(id_tutor,))
            result_habilidades=cursor.fetchall()
            for row_hab in result_habilidades:
                if row_hab[0]:
                    content["habilidades"].append(row_hab[0])
            
            #agregamos el registro a la lista
            lista_tutores.append(content)
    
            
            
    
    return {
        'statusCode': 200,
        'body': json.dumps({"tutores":lista_tutores})
    }

