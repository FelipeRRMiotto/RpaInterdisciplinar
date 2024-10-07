import os
from datetime import datetime, timedelta, date
import psycopg2 as pg
import json

with open(os.path.dirname(__file__)+"/config/config.json", 'r') as file:
    configs = json.load(file)


host_cloud = configs['host_cloud']
porta = configs['porta']
usuario = configs['usuario']
senha = configs['senha']
prod1 = configs['prod1']
prod2 = configs['prod2']
dev1 = configs['dev1']
dev2 = configs['dev2']

hoje = date.today()
timestampa = str(hoje)+"_"+str(datetime.now().strftime('%Hh%Mm%Ss'))
ontem = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

caminho = os.path.dirname(__file__)+"/logs/log_"+timestampa+".txt"
log = open(caminho,"a")

def escrevelog(texto='',pref="",cond="P"):
    if cond == "P":
        log.write("\n"+pref+" - "+str(datetime.now().strftime('%H:%M:%S'))+" - "+str(texto))
    elif cond == "E":
        log.write("\n\n"+pref+" ERRO! - "+str(datetime.now().strftime('%H:%M:%S'))+str(texto))
    elif cond == "S":
        log.write("\n\n"+("="*30)+"\n\n")
    elif cond == "L":
        log.write("\n\n\n"+pref+" - "+str(datetime.now().strftime('%H:%M:%S'))+" - "+str(texto))

log.write("Execução dia "+timestampa)
escrevelog(cond="S")

#O loop roda 2 vezes, a primeira no ambiente produtivo e a segunda no ambiente de dev
for amb in ["prd","dev"]:
    if amb == "prd":
        database1 = prod1
        database2 = prod2

        escrevelog("Processo no banco prd",pref=amb)
        print("Começando processo banco prd")
    else:
        database1 = dev1
        database2 = dev2


        escrevelog("Processo no banco dev",pref=amb)
        print("Começando processo banco dev")

    try:
        #criando conexões no banco
        escrevelog("Conectando no banco do 1°",pref=amb)
        conn1 = pg.connect(host=host_cloud, database=database1, user=usuario, password=senha, port=porta)
        escrevelog("Conectando no banco do 2°",pref=amb)
        conn2 = pg.connect(host=host_cloud, database=database2, user=usuario, password=senha, port=porta)
        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        #============================================================================================
        #Passando novos registros do banco do 1° para o banco do 2°
        #============================================================================================

        escrevelog("Passando novos registros do banco do 1° para o banco do 2°",pref=amb, cond="L")


        # Obtendo dados da tabela tb_cor_mascote do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_cor_mascote",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Insert tb_cor_mascote")

        cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria, deletedAt from tb_cor_mascote where createdAt = current_date-1')
        cores = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(cores) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            escrevelog("Inserindo registros", pref=amb)

            query = "INSERT INTO tb_cor_araci(pk_int_id_cor_araci, var_fundo, var_secundaria, var_primaria, deletedAt) values "
            for i in cores:
                query = query+"("+str(i[0])+",'"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"',"+str(i[4])+"),"
            query = ((query[:-1]).replace("'None'","null")).replace("None","null")
            cur2.execute(query)
            conn2.commit()

            escrevelog("Registros inseridos com sucesso", pref=amb)
        else:
            escrevelog("Nenhum novo registro encontrado",pref=amb)

        #===========================================================================================

        #Obtendo dados da tabela tb_evento do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_evento",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Insert tb_evento")

        cur1.execute('select dt_inicio, dt_final, var_nome, var_local, num_preco_ticket, pk_int_id_evento, fk_int_id_usuario, deletedat from tb_evento where createdAt = current_date-1')
        eventos = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(eventos) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            escrevelog("Inserindo registros", pref=amb)

            query = "INSERT INTO tb_evento(dt_data_inicio, dt_data_final, var_nome, var_local, float_preco_ticket, pk_int_id_evento, fk_int_id_usuario, deletedat) values "
            for i in eventos:
                query = query+"('"+str(i[0])+"','"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"',"+str(i[4])+","+str(i[5])+","+str(i[6])+","+str(i[7])+"),"
            query = ((query[:-1]).replace("'None'","null")).replace("None","null")
            cur2.execute(query)
            conn2.commit()

            escrevelog("Registros inseridos com sucesso", pref=amb)
        else:
            escrevelog("Nenhum novo registro encontrado",pref=amb)

        # #===========================================================================================

        #Obtendo dados da tabela tb_barraca do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_barraca",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Insert tb_barraca")

        cur1.execute('select pk_int_id_barraca, var_nome, fk_int_id_evento, deletedat from tb_barraca where createdAt = current_date-1')
        barracas = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(barracas) > 0:
            #Inserindo todos os registros encontrados no banco do 2°
            escrevelog("Inserindo registros", pref=amb)

            query = "INSERT INTO tb_barraca(pk_int_id_barraca, var_nome, fk_int_id_evento, deletedAt) values "
            for i in barracas:
                query = query+"("+str(i[0])+",'"+str(i[1])+"',"+str(i[2])+","+str(i[3])+"),"
            query = ((query[:-1]).replace("'None'","null")).replace("None","null")
            cur2.execute(query)
            conn2.commit()

            escrevelog("Registros inseridos com sucesso", pref=amb)
        else:
            escrevelog("Nenhum novo registro encontrado",pref=amb)
        
        escrevelog(cond="S")
        #============================================================================================
        #Passando registros recentemente alterados do banco do 1° para o banco do 2°
        #============================================================================================

        escrevelog("Passando registros alterados no banco do 1° para o banco do 2°",pref=amb)


        #Obtendo dados atualizados da tabela tb_cor_mascote do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_cor_mascote",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Update tb_cor_mascote")


        cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria, deletedAt from tb_cor_mascote where tb_cor_mascote.updateat = current_date-1 order by pk_int_id_cor_mascote')
        cores = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(cores) > 0:
            escrevelog("Obtendo os registros equivalentes do banco do 2°",pref=amb)

            lista_cols = ["var_primaria","var_secundaria","var_fundo","deletedAt"]
            lista_mods = []
            querySelect = "select var_fundo, var_secundaria, var_primaria, deletedAt from tb_cor_araci where pk_int_id_cor_araci in ("
            for i in cores:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_cor_araci"
            cur2.execute(querySelect)
            cores2 = cur2.fetchall()

            escrevelog("Comparando Registros e salvando alterações a serem feitas",pref=amb)

            for i in range(0,len(cores2)):
                for c in range(0,len(cores2[i])):
                    if cores2[i][c] != cores[i][c+1]:
                        lista_mods.append([lista_cols[c],cores[i][c+1],cores[i][0]])
            
            escrevelog("Realizando alterações",pref=amb)
            for i in lista_mods:
                query = (("update tb_cor_araci set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_cor_araci = "+str(i[2])).replace("'None'","null")).replace("None","null")
                cur2.execute(query)
            conn2.commit()
            escrevelog("Alterações realizadas com sucesso",pref=amb)
        else:
            escrevelog("Nenhum dado alterado encontrado",pref=amb)

        #===========================================================================================

        # Obtendo dados atualizados da tabela tb_evento do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_evento",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Update evento")

    
        cur1.execute('select pk_int_id_evento, dt_inicio, dt_final, var_nome, var_local, num_preco_ticket, deletedat, fk_int_id_usuario from tb_evento where tb_evento.updateat = current_date-1 order by pk_int_id_evento')
        eventos = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(eventos) > 0:
            escrevelog("Obtendo os registros equivalentes do banco do 2°",pref=amb)


            lista_cols = ["dt_data_inicio", "dt_data_final", "var_nome", "var_local", "float_preco_ticket", "deletedat", "fk_int_id_usuario"]
            lista_mods = []
            querySelect = "select dt_data_inicio, dt_data_final, var_nome, var_local, float_preco_ticket, deletedat, fk_int_id_usuario from tb_evento where pk_int_id_evento in ("
            for i in eventos:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_evento"
            cur2.execute(querySelect)
            eventos2 = cur2.fetchall()


            escrevelog("Comparando Registros e salvando alterações a serem feitas",pref=amb)

            for i in range(0,len(eventos2)):
                for c in range(0,len(eventos2[i])):
                    if eventos[i][c] != eventos[i][c+1]:
                        if c in [4,6]:
                            lista_mods.append([lista_cols[c],eventos[i][c+1],eventos[i][0]])
                        else:
                            lista_mods.append([lista_cols[c],"'"+str(eventos[i][c+1])+"'",eventos[i][0]])
            
            escrevelog("Realizando alterações",pref=amb)
            for i in lista_mods:
                query = (("update tb_evento set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_evento = "+str(i[2])).replace("'None'","null")).replace("None","null")
                cur2.execute(query)
            conn2.commit()
            escrevelog("Alterações realizadas com sucesso",pref=amb)
        else:
            escrevelog("Nenhum dado alterado encontrado",pref=amb)

        #===========================================================================================

        #Obtendo dados atualizados da tabela tb_barraca do banco do 1° e passando para o banco do 2°
        escrevelog("Obtendo dados da tabela tb_barraca",pref=amb, cond="L")
        print(database1+"---->"+database2+" // Update tb_barraca")


        cur1.execute('select pk_int_id_barraca, var_nome, deletedat, fk_int_id_evento from tb_barraca where updateat = current_date-1 order by pk_int_id_barraca')
        barracas = cur1.fetchall()

        #Verificando se algum novo registro foi encontrado
        if len(barracas) > 0:
            escrevelog("Obtendo os registros equivalentes do banco do 2°",pref=amb)


            lista_cols = ["var_nome", "deletedat", "fk_int_id_evento"]
            lista_mods = []
            querySelect = "select var_nome, deletedat, fk_int_id_evento from tb_barraca where pk_int_id_barraca in ("
            for i in barracas:
                querySelect = querySelect+str(i[0])+","
            querySelect = (querySelect[:-1])+") order by pk_int_id_barraca"
            cur2.execute(querySelect)
            barracas2 = cur2.fetchall()


            escrevelog("Comparando Registros e salvando alterações a serem feitas",pref=amb)

            for i in range(0,len(barracas2)):
                for c in range(0,len(barracas2[i])):
                    if barracas[i][c] != barracas[i][c+1]:
                        if c == 2:
                            lista_mods.append([lista_cols[c],barracas[i][c+1],barracas[i][0]])
                        else:
                            lista_mods.append([lista_cols[c],"'"+str(barracas[i][c+1])+"'",barracas[i][0]])
            
            escrevelog("Realizando alterações",pref=amb)
            for i in lista_mods:
                query = (("update tb_barraca set "+str(i[0])+" = "+str(i[1])+" where pk_int_id_barraca = "+str(i[2])).replace("'None'","null")).replace("None","null")
                cur2.execute(query)
            conn2.commit()
            escrevelog("Alterações realizadas com sucesso",pref=amb)
        else:
            escrevelog("Nenhum dado alterado encontrado",pref=amb)

        
        #============================================================================================
        #Passando novos registros do banco do 2° para o banco do 1°
        #============================================================================================
        # escrevelog(cond="S")
        # escrevelog("Passando novos registros do banco do 2° para o banco do 1°",pref=amb, cond="L")


        # # Obtendo dados da tabela tb_usuario do banco do 2° e passando para o banco do 1°
        # escrevelog("Obtendo dados da tabela tb_usuario",pref=amb, cond="L")
        # print(database2+"---->"+database1+" // Insert tb_usuario")

        # cur2.execute('select pk_int_id_usuario, var_foto, var_email, var_senha, var_user_name, dt_nascimento, var_descricao_usuario, var_cpf, var_nome, deletedAt from tb_usuario where createdAt = current_date-1')
        # usuarios = cur2.fetchall()

        # #Verificando se algum novo registro foi encontrado
        # if len(usuario) > 0:
        #     #Inserindo todos os registros encontrados no banco do 1°
        #     escrevelog("Inserindo registros", pref=amb)

        #     query = "insert into tb_usuario(pk_int_id_usuario, text_foto, var_email, var_senha, var_user_name, dt_nascimento, var_descricao_usuario, var_cpf, var_nome, deletedAt, createdAt) values "
        #     for i in usuario:
        #         query = query+"("+str(i[0])+",'"+str(i[1])+"','"+str(i[2])+"','"+str(i[3])+"','"+str(i[4])+"','"+str(i[5])+"','"+str(i[6])+"','"+str(i[7])+"','"+str(i[8])+"','"+str(i[9])+"',current_date),"
        #     query = ((query[:-1]).replace("'None'","null")).replace("None","null")
        #     cur1.execute(query)
        #     conn1.commit()

        #     escrevelog("Registros inseridos com sucesso", pref=amb)
        # else:
        #     escrevelog("Nenhum novo registro encontrado",pref=amb)

        

        # escrevelog("Passando novos registros do banco do 2° para o banco do 1°",pref=amb, cond="L")

        # # Obtendo dados da tabela tb_mascote do banco do 2° e passando para o banco do 1°
        # escrevelog("Obtendo dados da tabela tb_mascote",pref=amb, cond="L")
        # print(database2+"---->"+database1+" // Insert tb_mascote")

        # cur2.execute('select pk_int_id_mascote, var_nome, deletedAt, fk_int_id_cor_araci, fk_int_id_usuario from tb_mascote where createdAt = current_date-1')
        # mascotes = cur2.fetchall()

        # #Verificando se algum novo registro foi encontrado
        # if len(mascotes) > 0:
        #     #Inserindo todos os registros encontrados no banco do 1°
        #     escrevelog("Inserindo registros", pref=amb)

        #     query = "insert into tb_mascote(pk_int_id_mascote, var_nome, deletedAt, fk_int_id_cor_mascote, fk_int_id_usuario, createdAt) values "
        #     for i in mascotes:
        #         query = query+"("+str(i[0])+",'"+str(i[1])+"','"+str(i[2])+"',"+str(i[3])+","+str(i[4])+",current_date),"
        #     query = ((query[:-1]).replace("'None'","null")).replace("None","null")
        #     cur1.execute(query)
        #     conn1.commit()

        #     escrevelog("Registros inseridos com sucesso", pref=amb)
        # else:
        #     escrevelog("Nenhum novo registro encontrado",pref=amb)

        

    except (pg.Error) as error:
        print("Erro banco: ", error)
        escrevelog(error,pref=amb,cond="E")
    except (Exception) as error:
        print("Erro código python")
        escrevelog(error,pref=amb,cond="E")

    finally:
        if conn1:
            cur1.close()
            conn1.close()
            escrevelog("Conexão banco 1° encerrada",pref=amb,cond="L")
        if conn2:
            cur2.close()
            conn2.close()
            escrevelog("Conexão banco 2° encerrada",pref=amb)
        print("Conexões encerradas\n\n")
        escrevelog(cond="S")