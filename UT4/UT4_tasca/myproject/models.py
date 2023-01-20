from myproject import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import pymysql.cursors

# En heretar l'UserMixin, tenim accés a molts atributs integrats
# que podrem cridar en les nostres vistes!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()

# El decorador user_loader permet a flask-login carregar l'usuari actual
# i agafa el seu identificador.

@login_manager.user_loader
def load_user(user_id):
    #print("EN EXECUCIÓ - load_user")
    if user_id:
        userLM=User()
        userLM.obtenirDadesUserLM(user_id)
        print('DADES userLM')
        print(userLM.id)
        print(userLM.nomUsuari)
        #print(userLM.nom)
        #print(userLM.llinatges)
        #print(userLM.password)
        #print(userLM.data_alta)
        #print(userLM.email)
        #print(userLM.telefon)
        return userLM

# Cream CLASSE User
class User(UserMixin):

    id = 0

    # CONSTRUCTOR
    def __init__(self):
        self.nomUsuari="null"
    
    def set_nomUsuari(self, usuari):
        self.nomUsuari = usuari
    
    def comprovaPassword(self, password):
        #print("EN EXECUCIÓ - comprova password")
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT count(*) FROM usuaris WHERE username='"+self.nomUsuari+"'"
        cursor.execute(sql)
        resultatConsulta1=cursor.fetchone()
        if resultatConsulta1['count(*)']==1:
            # Existeix un únic registre amb aquest usuari
            sql = "SELECT password FROM usuaris WHERE username='"+self.nomUsuari+"'"
            cursor.execute(sql)
            resultatConsulta2=cursor.fetchone()
            # Resposta pot ser TRUE (password->OK) o FALSE (password->KO)
            resposta = check_password_hash(resultatConsulta2['password'],password)
        # NO existeix cap registre amb aquest usuari o més d'un registre
        else:
             resposta=False
        db.close()
        return resposta
    
    def obtenirDadesUsuariSegonsNomUsuari(self):
        #print("EN EXECUCIÓ - obtenirDadesUsuariSegonsNomUsuari")
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT * FROM usuaris WHERE username='"+self.nomUsuari+"'"
        cursor.execute(sql)
        resultatConsulta=cursor.fetchone()
        if resultatConsulta:
            self.id=resultatConsulta['idusuari']
        db.close() 
    
    
    def obtenirDadesUserLM(self,userid):
        #print("EXECUCIO obtenirDadesUserLM")
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        sql = "SELECT * FROM usuaris WHERE idusuari="+str(userid)
        cursor.execute(sql)
        resultatConsulta=cursor.fetchone()
        if resultatConsulta:
            self.id=resultatConsulta['idusuari']
            self.nomUsuari=resultatConsulta['username']
            self.nom=resultatConsulta['nom']
            self.llinatges=resultatConsulta['llinatges']
            self.password=resultatConsulta['password']
            self.data_alta=resultatConsulta['data_alta']
            self.email=resultatConsulta['email']
            self.telefon=resultatConsulta['telefon']
        db.close()

    def obtenirDarrerIdClient(self):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT MAX(idclient) maxId FROM clients;"
        cursor.execute(sql)
        darrerID=cursor.fetchone()
        db.close()
        return darrerID
    
      
        
        

    def altaUsuari(self,username,nom,llinatges,password,dataAlta,email,telefon):
        # CONNEXIO A BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)
        cursor=db.cursor()
        
        # Perque la TASCA DWES3 pugui seguir funcionant, en el mateix moment que
        # inserim un nou usuari en taula usuaris, també ho farem en la taula clients
        # fent que ambdos IDs coincideixin (idclient=idusuari)
        
        # Obtenim el darrer o el màxim idclient en la taula clients 
        darrerID=self.obtenirDarrerIdClient()
        # print(darrerID['maxId'])
        # Nou ID a assignar
        nouId=darrerID['maxId']+1
        # print(nouId)
        
        # Generam el HASH del password
        passwordHash=generate_password_hash(password)
        # print(passwordHash)
        
        # print(type(dataAlta))
        # print(dataAlta)
        # Convertim dataAlta en string
        stringData = dataAlta.strftime("%Y-%m-%d")
        
        # Eliminam espais en telefom
        telefonSenseEspais = telefon.replace(" ","")
        # print(telefonSenseEspais)
        
        # Inserim nou registre en taula usuaris
        sql="INSERT INTO usuaris VALUES ("+str(nouId)+",'"+username+"','"+nom+"','"+llinatges+"','"+passwordHash+"','"+stringData+"','"+email+"','"+telefonSenseEspais+"')"
        #print(sql)
        cursor.execute(sql)
        
        # Inserim nou registre en taula clients
        # Cal modificar en la taula clients, la longitud dels camps següents:
        # nom varchar(30)
        # telefon varchar (25)
        # per evitar inconsistències
        sql="INSERT INTO clients VALUES ("+str(nouId)+",'"+nom+"','"+llinatges+"','"+telefonSenseEspais+"')"
        #print(sql)
        cursor.execute(sql)
        
        db.close()
         
        
        
        
        

    







""" 
class gimnas(object):

    def carregaClients():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT * FROM clients"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def carregaPistes():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT * FROM pistes"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def carregaReserves():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT * FROM reserves"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def afegeixReserva(dataReserva,idPistaReserva,idClientReserva):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="INSERT INTO reserves (data,idpista,idclient)"
        sql=sql+" VALUES ('"+dataReserva+"',"+str(idPistaReserva)+","+str(idClientReserva)+");"
        cursor.execute(sql)
        db.close

    def carregaReservesSetmana(diaInici,diaFinal):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT reserves.data,reserves.idpista,reserves.idclient,pistes.tipo,"
        sql=sql+"clients.nom,clients.llinatges FROM reserves"
        sql=sql+" INNER JOIN pistes ON reserves.idpista=pistes.idpista"
        sql=sql+" INNER JOIN clients ON reserves.idclient=clients.idclient"
        sql=sql+" WHERE data BETWEEN '"+diaInici+"' AND '"+diaFinal+"'"
        sql=sql+" ORDER BY reserves.data ASC;"
        #print(sql)
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery

    def carregaClients():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT * FROM clients"
        cursor.execute(sql)
        ResQuery=cursor.fetchall()
        db.close()
        return ResQuery


    def tornaNumReservesClient(idclient):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT COUNT(idclient) FROM reserves WHERE idclient="+str(idclient)+";"
        cursor.execute(sql)
        num=cursor.fetchone()
        db.close()
        return num

    def eliminaClient(idclient):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="DELETE FROM clients WHERE idclient="+str(idclient)+";"
        cursor.execute(sql)
        db.close()

    def tornaMaximIdclient():
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="SELECT MAX(idclient) maxId FROM clients;"
        cursor.execute(sql)
        Id=cursor.fetchone()
        db.close()
        return Id

    def afegeixClient(idclient,nom,llinatges,telefon):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="INSERT INTO clients (idclient,nom,llinatges,telefon)"
        sql=sql+" VALUES ("+str(idclient)+",'"+nom+"','"+llinatges+"','"+telefon+"');"
        cursor.execute(sql)
        db.close()

    def modificaClient(idclient,nom,llinatges,telefon):
        # connexxió a BBDD
        db=pymysql.connect(host='localhost',
                            user='root',
                            db='gimnas',
                            charset='utf8mb4',
                            autocommit=True,
                            cursorclass=pymysql.cursors.DictCursor)

        cursor=db.cursor()
        sql="UPDATE clients SET nom='"+nom+"',llinatges='"+llinatges+"',"
        sql=sql+"telefon='"+telefon+"' WHERE idclient="+str(idclient)+";"
        cursor.execute(sql)
        db.close

 """