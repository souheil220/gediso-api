import psycopg2

class Connexion: 
    def connect():
        conn_string = "host='10.20.10.43' dbname='gediso_document' user='odoo' password='odoo_hasnaoui_2021'"
        print ("Connecting to database\n	->%s" % (conn_string))
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        return cursor
        
    
    def getRequisition(self,id):
        cursor = self.connect()
        cursor.execute('''
                    select id,record_id,col_3094,col_3095,
                        col_3096,col_3097,col_3098,
                        col_3099,col_3100,col_3101,col_3102 
                     from doc_id_160 
                     where record_id=%s'''
                    %id)
        
        records = cursor.fetchall()
        cursor.close()
        return records[0]

    def getAutorisationDeSortie(self,id):
        cursor = self.connect()
        cursor.execute('''
                    select 
                         id,record_id,
                        col_774,col_777,
                        col_2345,col_2461,col_2464,
                        col_2465,col_3943,
                        col_4074,col_4095 ,
                        col_4177,col_4178 
                    from doc_id_55 
                    where record_id=%s'''
                    %id)
        
        records = cursor.fetchall()
        cursor.close()
        return records[0]

    def getDemandeDappro(self,id):
        cursor = self.connect()
        cursor.execute('''
                    select 
                        di136.id,di136.record_id,
                        col_2019,col_2020,
                        col_2474,col_4892,
                        col_2022,col_7592,col_7652,
                        col_7594
                    from doc_id_136 as di136
                    inner join doc_id_136_table_id_131 as diti on di136.id = diti.document_id  
                    where record_id=%s'''
                    %id)
        
        records = cursor.fetchall()
        cursor.close()
        return records

class ConnexionOdoo:
    def connect():
        conn_string = "host='10.20.10.43' dbname='hasnaoui' user='odoo' password='odoo_hasnaoui_2021'"
       
        print ("Connecting to database\n	->%s" % (conn_string))
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        return cursor

    def getGedisoDocumentRecord(self,id):
        cursor = self.connect()
        cursor.execute("""
                        select * 
                          from CROSSTAB ('
                                SELECT 
                                record_id,
                                id, 
                                user_id
    	                        FROM public."DOCULMENT_VALIDATION_CYCLE"
    	                        where "record owner" IN (2031) and document_id IN (%s)
			                    order by 1,2' )
                                AS T(record_id int, 
                                    validation_user_1 int,
                                    validation_user_2 INT,
                                    validation_user_3 INT,
                                    validation_user_4 INT,
                                    validation_user_5 INT)
                        LEFT join (select 
                                        distinct id,
                                        TO_CHAR(create_date:: DATE, 'dd/mm/yyyy') "create_date",
                                        document_id,state,
                                        attachment_id,
                                        record_id,
                                        "record owner",
                                        name 
                                    from public."DOCULMENT_VALIDATION_CYCLE")as dvc 
                        on T.record_id = dvc.record_id
                        order by dvc.create_date desc"""%id)
        records = cursor.fetchall()
        cursor.close()
        return records
       

    def getUserParentId(self,id):
        cursor = self.connect()
        cursor.execute("""select user_id,login from hr_employee he
                            left join hr_employee he2  on he.parent_id = he2.id  
                            left join resource_resource rr on he2.resource_id  = rr.id  
                            left join res_users ru on rr.user_id = ru.id
                            where he.matricule  = '009458'""")
        records = cursor.fetchall()
        cursor.close()
        return records

    def getValidationCycle(self,id):
        cursor = self.connect()
        cursor.execute("""SELECT 	
                            gvd.user_id,
                            ru.login 
                            FROM public.gediso_validation_document gvd
                            left join res_users ru on gvd.user_id = ru.id 
                            where document_id =%s and gvd.active = true and gvd.company_id =1
                            order by --rc."name" ,
                            gvd."sequence" asc"""%id)
        records = cursor.fetchall()
        cursor.close()
        return records
