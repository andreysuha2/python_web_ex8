from connect import connect
from models import Quote, Author

author = Author.objects(fullname="Steve Martin").first()

print(author.quotes)