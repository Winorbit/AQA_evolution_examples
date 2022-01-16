import re
# from .settings import logger
# from settings import logger


def check_email(email: str):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(email_regex,email)):  
        # logger.info(f"Email {email} is valid")
        return True  
    else: 
        # logger.error(f"Email {email} is invalid")
        return False