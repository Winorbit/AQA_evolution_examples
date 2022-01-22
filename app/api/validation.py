import re
import sys

called_from = sys.modules['__main__'].__file__
if "unittest" in called_from or "pytest" in called_from:
    from .settings import logger
else:
    from settings import logger

def check_email(email: str):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(email_regex,email)):  
        logger.info(f"Email {email} is valid")
        return True  
    else: 
        logger.error(f"Email {email} is invalid")
        return False