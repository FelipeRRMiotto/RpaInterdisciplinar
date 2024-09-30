from datetime import date
import psycopg2 as pg

hoje = str(date.today())
host_cloud = "pg-11d01e0e-testepgsql.e.aivencloud.com"
porta = "24931"
usuario = "avnadmin"
senha = "AVNS_69W0O2_65jEqbsCuztW"
prod1 = 'banco1_prod'
prod2 = 'banco2_prod'
dev1 = 'banco1_dev'
dev2 = 'banco2_dev'


for amb in range(0,2):
    if amb == 0:
        database1 = prod1
        database2 = prod2
    else:
        database1 = dev1
        database2 = dev2

    try:
        conn1 = pg.connect(host=host_cloud, database=database1, user=usuario, password=senha, port=porta)
        conn2 = pg.connect(host=host_cloud, database=database2, user=usuario, password=senha, port=porta)
        cur1 = conn1.cursor()
        cur2 = conn2.cursor()

        cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria from tb_cor_mascote where createdAt < %s',(hoje,))
        cores = cur1.fetchall()

        if len(cores) > 0:
            query = "INSERT INTO tb_cor_araci(pk_int_id_cor_araci, var_fundo, var_secundaria, var_primaria) values "
            for i in cores:
                    query = query+"("+i[0]+","+i[1]+","+i[2]+","+i[3]+"),"
            query = query[:-1]
            cur2.execute(query)

        cur1.execute('select dt_data_inicio, dt_data_final, var_nome, var_local, num_preco_ticket, pk_int_id_evento, fk_int_id_usuario from tb_evento where createdAt < %s',(hoje,))
        cores = cur1.fetchall()

        if len(cores) > 0:
            query = "INSERT INTO tb_cor_araci(pk_int_id_cor_araci, var_fundo, var_secundaria, var_primaria) values "
            for i in cores:
                    query = query+"("+i[0]+","+i[1]+","+i[2]+","+i[3]+"),"
            query = query[:-1]
            cur2.execute(query)
        

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