from sqlite3 import connect
#FUNCTIONS

#create registredbotuser
def createregistredbotuser(phone,user_id,username):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    phone = int(phone)
    user_id = int(user_id)
    username = str(username)
    user = cur.execute(f"""
                        INSERT INTO vote_registredbotuser(phone,userid,username,checked,allowed,age)
                        VALUES({phone},{user_id},"{username}",False,False,18)
                        """)
    con.commit()
    con.close()

#check registredbotuser
def checkregistredbotuser(user_id):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    user = cur.execute(f"""
                        SELECT * FROM vote_registredbotuser WHERE userid={user_id}
                        """).fetchone()
    con.close()
    if user is None:
        return False
    else:
        return True



#get registred user from registredbotuser
def getregistredbotuser(user_id):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    user = cur.execute(f"""
                        SELECT * FROM vote_registredbotuser WHERE userid={user_id}
                        """).fetchone()
    data = {
        "id":user[0],
        "phone":user[1],
        "user_id":user[2],
        "username":user[3],
        "allowed":user[4],
        "checked":user[5],
        "age":user[6]
            }
    con.close()
    return data

#img word create
def imgword(user_id,text):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    text = str(text)
    exists = cur.execute(f"""
                         SELECT userid FROM vote_imgwrod WHERE userid={user_id}
                         """).fetchone()

    if exists is None:
        cur.execute(f"""
                        INSERT INTO vote_imgwrod(userid,text)
                        VALUES({user_id},"{text}")
                    """)
    else:
        cur.execute(f"""
                        UPDATE vote_imgwrod SET text = "{text}" WHERE userid={user_id}
                    """)
    con.commit()
    con.close()

def imgwordcheck(user_id):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    text = cur.execute(f"""
                SELECT text FROM vote_imgwrod WHERE userid={user_id}
                """).fetchone()
    con.close()
    return text[0]
#update checked user
def updatecheckeduser(user_id):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    cur.execute(f"""
                UPDATE vote_registredbotuser SET checked = True WHERE userid={user_id}
                """)
    cur.execute(f"""
                DELETE FROM vote_imgwrod WHERE userid={user_id}
                """)
    con.commit()
    con.close()

#update user age
def updateuserage(user_id,age):
    user_id = int(user_id)
    age = int(age)
    con = connect("../db.sqlite3")
    cur = con.cursor()
    cur.execute(f"""
                UPDATE vote_registredbotuser SET age={age} WHERE userid={user_id}   
                """)
    con.commit()
    con.close()

#update allowed user
def updatealloweduser(user_id):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user_id = int(user_id)
    cur.execute(f"""
                UPDATE vote_registredbotuser SET allowed = True WHERE userid={user_id}
                """)
    con.commit()
    con.close()

#get all category
def getallcategory():
    con = connect("../db.sqlite3")
    cur = con.cursor()
    category = cur.execute(f"""
                            SELECT * FROM vote_category
                            """).fetchall()
    data = []
    for i in category:
        data.append({
                    "id":i[0],
                    "name":i[1],
                    "date":i[2]
                    }
                    )
    con.close()
    return data

#get bind all places
def getcategoryplaces(category_name):
    con = connect("../db.sqlite3")
    cur = con.cursor()
    category_name = str(category_name)
    category_id = cur.execute(f"""
                                SELECT id FROM vote_category WHERE name="{category_name}"
                               """).fetchone()

    category_id = int(category_id[0])
    places = cur.execute(f"""
                            SELECT * FROM vote_places WHERE bind_id={category_id}
                          """).fetchall()

    data = []
    for i in places:
        data.append({
                    "id":i[0],
                    "name":i[1],
                    "voted":i[2],
                    "date":i[3],
                    "bind":i[4]
                     })
    con.close()
    return data

def getcategorybyplname(place_name):
    place_name = str(place_name)
    con = connect("../db.sqlite3")
    cur = con.cursor()

    plid = cur.execute(f"""
                            SELECT bind_id FROM vote_places WHERE name="{place_name}"
                            """).fetchone()

    plid = int(plid[0])
    category = cur.execute(f"""
                            SELECT name FROM vote_category WHERE id={plid}
                            """).fetchone()

    con.close()
    return category[0]


def getbotuser(places_name,user_id,name):
    import datetime
    con = connect("../db.sqlite3")
    cur = con.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    user_id = int(user_id)
    places_name = str(places_name)
    name = str(name)
    place_bind_id = cur.execute(f"""
                                SELECT bind_id FROM vote_places WHERE name="{places_name}"
                                """).fetchone()

    place_bind_id = int(place_bind_id[0])

    usercategory = cur.execute(f"""
                                SELECT category_id FROM vote_botuser WHERE userid={user_id}
                                """).fetchall()

    def createbotuserincrement():
        updateplaces = cur.execute(f"""
                                    UPDATE vote_places SET vote = vote+1 WHERE name="{places_name}"
                                    """)

        registred = getregistredbotuser(user_id)

        plid = cur.execute(f"""
                            SELECT id FROM vote_places WHERE name="{places_name}"
                            """).fetchone()

        plid = int(plid[0])

        res = cur.execute(f"""
                            INSERT INTO vote_botuser(phonenumber,userid,username,name,voted_id,category_id,date,age)
                            VALUES({registred.get("phone")},{user_id},"{registred.get("username")}","{name}",{plid},{place_bind_id},"{date}",{registred.get("age")})
                          """)


        con.commit()


    if usercategory == []:
        createbotuserincrement()
        con.close()
        return True
    else:
        if place_bind_id in [x[0] for x in usercategory]:
            con.close()
            return False
        else:
            createbotuserincrement()
            con.close()
            return True

#check allow user
def checkallowuser(user_id):
    user_id = int(user_id)
    con = connect("../db.sqlite3")
    cur = con.cursor()
    user = cur.execute(f"""
                SELECT allowed FROM vote_registredbotuser WHERE userid={user_id}
                """).fetchone()
    con.close()
    return user[0]