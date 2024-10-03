from datetime import datetime, timedelta, date
import psycopg2 as pg

ontem = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

host_cloud = "pg-11d01e0e-testepgsql.e.aivencloud.com"
porta = "24931"
usuario = "avnadmin"
senha = "AVNS_69W0O2_65jEqbsCuztW"
prod1 = 'banco1_prod'
prod2 = 'banco2_prod'
dev1 = 'banco1_dev'
dev2 = 'banco2_dev'


#O loop roda 2 vezes, a primeira no ambiente produtivo e a segunda no ambiente de dev
for amb in range(0,2):
    if amb == 0:
        database1 = prod1
        database2 = prod2

        print("Começando processo banco prd")
    else:
        database1 = dev1
        database2 = dev2
        print("Começando processo banco dev")

    try:
        #criando conexões no banco
        conn1 = pg.connect(host=host_cloud, database=database1, user=usuario, password=senha, port=porta)
        conn2 = pg.connect(host=host_cloud, database=database2, user=usuario, password=senha, port=porta)
        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        #============================================================================================
        #Passando novos registros do banco do 1° para o banco do 2°
        #============================================================================================

        # Obtendo dados da tabela tb_cor_mascote do banco do 1° e passando para o banco do 2°
        cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria, deletedAt from tb_cor_mascote where createdAt = %s',(ontem,))
        cores = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(cores) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            query = "INSERT INTO tb_cor_araci(pk_int_id_cor_araci, var_fundo, var_secundaria, var_primaria, deletedAt) values "
            for i in cores:
                query = query+"("+str(i[0])+",'"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"',"+str(i[4])+"),"
            query = (query[:-1]).replace("'None'","null")
            cur2.execute(query)
            conn2.commit()

        #===========================================================================================

        #Obtendo dados da tabela tb_evento do banco do 1° e passando para o banco do 2°
        cur1.execute('select dt_inicio, dt_final, var_nome, var_local, num_preco_ticket, pk_int_id_evento, fk_int_id_usuario, deletedat from tb_evento where createdAt = %s',(ontem,))
        eventos = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(eventos) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            query = "INSERT INTO tb_evento(dt_data_inicio, dt_data_final, var_nome, var_local, float_preco_ticket, pk_int_id_evento, fk_int_id_usuario, deletedat) values "
            for i in eventos:
                query = query+"('"+str(i[0])+"','"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"',"+str(i[4])+","+str(i[5])+","+str(i[6])+","+str(i[7])+"),"
            query = (query[:-1]).replace("'None'","null")
            cur2.execute(query)
            conn2.commit()

        # #===========================================================================================

        #Obtendo dados da tabela tb_barraca do banco do 1° e passando para o banco do 2°
        cur1.execute('select pk_int_id_barraca, var_nome, fk_int_id_evento, deletedat from tb_barraca where createdAt = %s',(ontem,))
        barracas = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(barracas) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            query = "INSERT INTO tb_barraca(pk_int_id_barraca, var_nome, fk_int_id_evento, deletedAt) values "
            for i in barracas:
                query = query+"("+str(i[0])+",'"+str(i[1])+"',"+str(i[2])+","+str(i[3])+"),"
            query = (query[:-1]).replace("'None'","null")
            cur2.execute(query)
            conn2.commit()
        
        #============================================================================================
        #Passando registros recentemente alterados do banco do 1° para o banco do 2°
        #============================================================================================

        #Obtendo dados atualizados da tabela tb_cor_mascote do banco do 1° e passando para o banco do 2°
        print(database1+"---->"+database2+" // Update tb_cor_mascote")
        cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria, deletedAt from tb_cor_mascote where tb_cor_mascote.updateat = %s order by pk_int_id_cor_mascote',(ontem,))
        cores = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(cores) > 0:
            lista_cols = ["var_primaria","var_secundaria","var_fundo","deletedAt"]
            lista_mods = []
            querySelect = "select var_fundo, var_secundaria, var_primaria, deletedAt from tb_cor_araci where pk_int_id_cor_araci in ("
            for i in cores:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_cor_araci"
            cur2.execute(querySelect)
            cores2 = cur2.fetchall()

            for i in range(0,len(cores2)):
                for c in range(0,len(cores2[i])):
                    if cores2[i][c] != cores[i][c+1]:
                        lista_mods.append([lista_cols[c],cores[i][c+1],cores[i][0]])
            
            for i in lista_mods:
                query = ("update tb_cor_araci set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_cor_araci = "+str(i[2])).replace("'None'","null")
                cur2.execute(query)
            conn2.commit()
        else:
            print("Sem dados encontrados")

        #===========================================================================================

        # Obtendo dados atualizados da tabela tb_evento do banco do 1° e passando para o banco do 2°
        print(database1+"---->"+database2+" // Update evento")
        cur1.execute('select pk_int_id_evento, dt_inicio, dt_final, var_nome, var_local, num_preco_ticket, deletedat, fk_int_id_usuario from tb_evento where tb_evento.updateat = %s order by pk_int_id_evento',(ontem,))
        eventos = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(eventos) > 0:
            lista_cols = ["dt_data_inicio", "dt_data_final", "var_nome", "var_local", "float_preco_ticket", "deletedat", "fk_int_id_usuario"]
            lista_mods = []
            querySelect = "select dt_data_inicio, dt_data_final, var_nome, var_local, float_preco_ticket, deletedat, fk_int_id_usuario from tb_evento where pk_int_id_evento in ("
            for i in eventos:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_evento"
            cur2.execute(querySelect)
            eventos2 = cur2.fetchall()

            for i in range(0,len(eventos2)):
                for c in range(0,len(eventos2[i])):
                    if eventos[i][c] != eventos[i][c+1]:
                        if c in [4,6]:
                            lista_mods.append([lista_cols[c],eventos[i][c+1],eventos[i][0]])
                        else:
                            lista_mods.append([lista_cols[c],"'"+str(eventos[i][c+1])+"'",eventos[i][0]])
            
            for i in lista_mods:
                query = ("update tb_evento set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_evento = "+str(i[2])).replace("'None'","null")
                cur2.execute(query)
            conn2.commit()
        else:
            print("Sem dados encontrados")

        #===========================================================================================

        #Obtendo dados atualizados da tabela tb_barraca do banco do 1° e passando para o banco do 2°
        print(database1+"---->"+database2+" // Update tb_barraca")
        cur1.execute('select pk_int_id_barraca, var_nome, deletedat, fk_int_id_evento from tb_barraca where updateat = %s order by pk_int_id_barraca',(ontem,))
        barracas = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(barracas) > 0:
            lista_cols = ["var_nome", "deletedat", "fk_int_id_evento"]
            lista_mods = []
            querySelect = "select var_nome, deletedat, fk_int_id_evento from tb_barraca where pk_int_id_barraca in ("
            for i in barracas:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_barraca"
            cur2.execute(querySelect)
            barracas2 = cur2.fetchall()

            for i in range(0,len(barracas2)):
                for c in range(0,len(barracas2[i])):
                    if barracas[i][c] != barracas[i][c+1]:
                        if c == 2:
                            lista_mods.append([lista_cols[c],barracas[i][c+1],barracas[i][0]])
                        else:
                            lista_mods.append([lista_cols[c],"'"+str(barracas[i][c+1])+"'",barracas[i][0]])
            
            for i in lista_mods:
                query = ("update tb_barraca set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_barraca = "+str(i[2])).replace("'None'","null")
                cur2.execute(query)
            conn2.commit()
        else:
            print("Sem dados encontrados")
        

    except (Exception, pg.Error) as error:
        print("Erro ao obter dados do banco: ", error)

    finally:
        if conn1:
            cur1.close()
            conn1.close()
        if conn2:
            cur2.close()
            conn2.close()
        print("Conexões encerradas")