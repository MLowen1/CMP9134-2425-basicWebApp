# Example for a file needing db:
# Original line: from extensions import db
from backend.extensions import db # Changed to absolute import

# Example for a file needing db and jwt:
# Original line: from extensions import db, jwt 
from backend.extensions import db, jwt # Changed to absolute import

# ...rest of the route file...
