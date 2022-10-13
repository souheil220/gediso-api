from flask import Flask,jsonify,request
from xmlrpc import client as xmlrpclib
from db import Connexion,ConnexionOdoo


app = Flask(__name__,static_folder='./images',)
# odoo
url = "http://10.20.10.42:8069"
dbo = "hasnaoui"
username = "admin"
password = "4g$1040"

models = xmlrpclib.ServerProxy("{}/xmlrpc/2/object".format(url))
common = xmlrpclib.ServerProxy("{}/xmlrpc/2/common".format(url))
uid = common.authenticate(dbo, username, password, {})

# gediso
# urlged = "http://10.20.10.43:8069"
# dboged = "gediso_document"
# usernameged = "odoo_document"
# passwordged = "odoo_document_2021"

# modelsged = xmlrpclib.ServerProxy("{}/xmlrpc/2/object".format(urlged))
# commonged = xmlrpclib.ServerProxy("{}/xmlrpc/2/common".format(urlged))
# uidged = commonged.authenticate(dboged, usernameged, passwordged, {})
# print(uidged)


@app.route("/")
def get_all_documents():
    document_id = int(request.args.get("document_id"))

    userParent = ConnexionOdoo.getUserParentId(ConnexionOdoo,document_id)
    

    cycleDeValidation = ConnexionOdoo.getValidationCycle(ConnexionOdoo,document_id)
   
    ids_list = []

    
    nameParent = userParent[0][1].split('.')
    for id in cycleDeValidation:
        if id[0] != None:
            nameValidator = id[1].split('.')
            ids_list.append({
                "user_id":id[0],
                "name":nameValidator[0].capitalize()+" " + nameValidator[1].split("@", 1)[0].capitalize(),
                "valide":None
                })
        else:
            ids_list.append({
                "user_id":userParent[0][0],
                "name":nameParent[0].capitalize()+" " + nameParent[1].split("@", 1)[0].capitalize(),
                "valide":None
                })
    

    ged_docs = ConnexionOdoo.getGedisoDocumentRecord(ConnexionOdoo,document_id)
    
    # deg_documents = models.execute_kw(
    #             dbo,
    #             uid,
    #             password,
    #             "gediso.document.record",
    #              "search_read",
    #             [[["user_id","=",2031],["document_id","=",document_id]
    #           ]], {"fields": ["document_id","state","attachment_id"]},)
    # return ([{"deg_documents":ged_docs , "validation_cycle":ids_list}])
    return ([{"deg_documents":ged_docs , "validation_cycle":ids_list}])

@app.route("/get_heure_sup")
def get_heure_supp_documents():
    id = int(request.args.get("record_id"))
    record = Connexion.getRequisition(Connexion,id)
    data = {
        "id":record[0],
        "record_id":record[1],
        "date_du_doc":str(record[2].strftime("%d/%m/%Y") ),
        "user":record[3],
        "cause":record[4],
        "heure_travaillé":record[5],
        "date_heure_supp":str(record[6].strftime("%d/%m/%Y")),
        "heure_debut":str(record[7])+"H "+str(record[8])+"min",
        "heure_fin":str(record[9])+"H "+str(record[10])+"min"
    }

    return jsonify(data) 

@app.route("/get_autorisation_de_sortie")
def get_autorisation_de_sortie():
    id = int(request.args.get("record_id"))
    record = Connexion.getAutorisationDeSortie(Connexion,id)
    print(record)
    data = {
        "id":record[0],
        "record_id":record[1],
        "cause":record[2],
        "heure_de_sortie":str(record[3])+"H "+str(record[4])+"min",
        "date_du_doc":str(record[5].strftime("%d/%m/%Y") ),
        "heure_de_retour":str(record[6])+"H "+str(record[7])+"min",
        "user":record[8],
        "la_durée_dabsence":str(record[9])+"H "+str(record[11])+"min",
        "date_de_sortie":str(record[10].strftime("%d/%m/%Y")),
        "date_de_retour":str(record[12].strftime("%d/%m/%Y"))
    }

    return jsonify(data) 

@app.route("/get_demande_dappro")
def get_demande_dappro():
    id = int(request.args.get("record_id"))
    record = Connexion.getDemandeDappro(Connexion,id)
    i=1
    data = {}
    for product in record:
        data[i] = {
            "designation_article":product[5],
            "date_souhaite_de_la_reception":str(product[6].strftime("%d/%m/%Y")),
            "um":product[7],
            "la_quantite_demande":product[8],
            "centre_de_cout":product[9]
            
        }
        i+=1
    data[i] = {
   "id":record[0][0],
   "record_id":record[0][1],
   "date_de_la_demande":str(record[0][2].strftime("%d/%m/%Y")),
   "user": record[0][3]   
    }
    
    print(data)
   

    return jsonify({"data":data}) 

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")