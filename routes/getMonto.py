from fastapi import APIRouter
from db.db import conn

calculadora = APIRouter()

@calculadora.get("/get_monto")
async def get_monto(id_acto = "-1", monto=0):
      

      json_tarifas={}
      detalle_tarifas = []
      total_honorarios = 0

      monto = float(monto)

      with conn.cursor(dictionary=True) as cursor:
        # Read a single record
        if (id_acto =="-1"):
          sql = "select * from acto a inner join registro_acto ra on a.id_acto = ra.acto_id_acto" 
        else:
          sql = 'select * from acto a inner join tarifario t ON a.id_acto = t.acto_id_acto inner join timbre t2 on t.timbre_id_timbre  = t2.id_timbre  where a.id_acto = '+ id_acto + ' order by t2.id_timbre;'
               
        # DEFINO UN CURSOR PARA RECORRER LAS TARIFAS DEL ACTO INDICADO 
        cursor.execute(sql)
        result = cursor.fetchall()
        
          
        tarifario = {
          'tarifa':0,
          'honorarios':0,
          'total_tarifas':0
        }


        for row in result:
           id_timbre = row['id_timbre']
           timbre_descripcion = row['timbre_descripcion']
           factor= str(row['factor'])
           valor= float(row['valor'])
           multiplo= float(row['multiplo'])
           minimo= float(row['minimo'])
           porcentaje = float(row['porcentaje'])
           timbre_id_rango_timbre = row['timbre_id_rango_timbre']

#TIMBRE DEFINIDO POR MULTIPLO

           if (factor =='M'):
                
                print(monto)
                print(valor)

                tarifa = (monto / valor) * multiplo
                tarifa = tarifa  * porcentaje
                if (tarifa < minimo): 
                    tarifa = minimo
                #end if    
            #end if

#TIMBRE DEFINIDO POR VALOR ABSOLUTO
           if (factor =='A'):
                tarifa = valor
                tarifa = tarifa  * porcentaje
           #end if

#TIMBRE DEFINIDO POR PORCENTAJE

           if (factor=='P'):
                tarifa = monto * valor
                tarifa = tarifa  * porcentaje
                if (tarifa < minimo): 
                    tarifa = minimo
                #end if
           #end if
# TIMBRE DEFINIDO POR RANGO
    
           if (factor =='R'):
                query_2 = "select * from rango_timbre rt where rt.id_rango_timbre = " +str(timbre_id_rango_timbre) +";" ; 
                
                with conn.cursor(dictionary=True) as cursor_rangos:
                    cursor_rangos.execute(query_2)
                    rangos = cursor_rangos.fetchall()
        
# RECORRO LOS DISTINTOS RANGOS QUE APLICAN 
                    for row_rango in rangos:
                        rango_minimo = row_rango['minimo']
                        rango_maximo = row_rango['maximo']
                        rango_valor = row_rango['valor']

                        if((monto > rango_minimo) and (monto <= rango_maximo)): 

                            tarifa  = rango_valor
                            tarifa =  tarifa * porcentaje
                        #end if
                    #end for - rangos
                    cursor_rangos.close()
            #end if 

           json_tarifas['id'] = id_timbre
           json_tarifas['descripcion'] = timbre_descripcion
           json_tarifas['tarifa'] = tarifa
           
           detalle_tarifas.append(json_tarifas.copy()) 

           total_honorarios+=tarifa

        #end for - tarifas    
        cursor.close()

#OBTENGO EL COSTO POR HONORARIOS 

      query_honorarios = 'select * from honorarios h order by id_honorario;' ; 
      with conn.cursor(dictionary=True) as cursor_honorarios:
        cursor_honorarios.execute(query_honorarios)
        detalle_honorarios = cursor_honorarios.fetchall()

        honorarios=0
        for row_honorarios in detalle_honorarios:
           
           minimo_honorarios = row_honorarios['minimo']
           maximo_honorarios = row_honorarios['maximo']
           porcentaje_honorarios = row_honorarios['porcentaje']

           if (monto > minimo_honorarios): 
                if (monto <= maximo_honorarios): 
                    honorarios  = (monto - minimo_honorarios) * porcentaje_honorarios + honorarios
                else:
                    honorarios = (maximo_honorarios - minimo_honorarios) * porcentaje_honorarios + honorarios
                #end if
            #end if
        cursor_honorarios.close()



# OBTENGO EL VALOR MINIMO HONORARIOS Y SI ES SUPERIOR AL VALOR ACTUAL, SE SUSTITUYE

        query_honorario_minimo = 'select valor from variables where id=2'; 
        with conn.cursor(dictionary=True) as cursor_honorario_minimo:
            cursor_honorario_minimo.execute(query_honorario_minimo)
            result_honorario_minimo = cursor_honorario_minimo.fetchone()

            minimo_honorarios = result_honorario_minimo['valor'] 
            
            cursor_honorario_minimo.close()
        
        if (honorarios<minimo_honorarios):
            honorarios= minimo_honorarios

        json_tarifas['id'] = '+'
        json_tarifas['descripcion'] = 'Honorarios'
        json_tarifas['tarifa'] = honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 
        
        total_honorarios+=honorarios

# OBTENGO EL VALOR DEL IVA 

        query_iva = 'select valor from variables where id=1'; 
        with conn.cursor(dictionary=True) as cursor_iva:
            cursor_iva.execute(query_iva)
            result_iva = cursor_iva.fetchone()

            iva = result_iva['valor'] 
            
            cursor_iva.close()
        
        iva_honorarios = honorarios*iva

        json_tarifas['id'] = '++'
        json_tarifas['descripcion'] = 'IVA Honorarios'
        json_tarifas['tarifa'] = iva_honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 

        total_honorarios+=iva_honorarios

        json_tarifas['id'] = '+++'
        json_tarifas['descripcion'] = 'Total Honorarios + timbres'
        json_tarifas['tarifa'] = total_honorarios
        
        detalle_tarifas.append (json_tarifas.copy()) 

        return(detalle_tarifas)
