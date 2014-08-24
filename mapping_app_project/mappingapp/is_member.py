# function for use in testing if user belongs to Super User group

def is_member(user):
    return user.groups.filter(name='Consortium Super User')
