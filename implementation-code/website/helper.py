import pickle as pk

def update_db(access_nature, db, username):
    if access_nature == "granted":
        update_field = "Logins"
    else:
        update_field = "Denied"

    with open(db, "rb") as f:
        creds_db = pk.load(f)
        ind = None
        for i, d in enumerate(creds_db):
            if d['username'] == username:
                ind = i
                break
    creds_db[ind][update_field] = creds_db[ind][update_field]+ 1
    return "updated"

def admin_load(db):
    with open("db.pk", "rb") as f:
        db = pk.load(f)
        db_list = db.copy()

    for data_dict in db_list[1:]:
        data_dict.pop("img")
    
    return db_list