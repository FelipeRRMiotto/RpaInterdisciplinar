from datetime import date
import psycopg2 as pg

hoje = date.today()
host_cloud = "pg-11d01e0e-testepgsql.e.aivencloud.com"
porta = "24931"
usuario = "avnadmin"
senha = "AVNS_69W0O2_65jEqbsCuztW"
database1 = 'banco1_prod'
database2 = 'banco2_prod'

try:
    conn1 = pg.connect(host=host_cloud, database=database1, user=usuario, password=senha, port=porta)
    cur1 = conn1.cursor()

    cur1.execute('select pk_int_id_cor_mascote, text_fundo, text_secundaria, text_primaria from tb_cor_mascote where createdAt < %s',(hoje))
    conn1.commit()
    cur1.close()
    conn1.close()

except (Exception, pg.Error) as error:
    print("Erro ao obter dados do banco", error)

finally:
    if conn1:
        cur1.close()
        conn1.close()
        print("Conexões encerradas")



conn2 = pg.connect(host=host_cloud, database=database2, user=usuario, password=senha, port=porta)

print(hoje)