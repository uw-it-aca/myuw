from myuw_mobile.dao.pws import Person as PersonDao

person_dao = PersonDao()

def get_regid(netid): 
    return person_dao.get_regid(netid)

def get_contact(regid):
    return person_dao.get_contact(regid)

def is_valid_netid(netid): 
    return get_regid(netid)

def is_student(netid): 
    return person_dao.is_student(netid)



