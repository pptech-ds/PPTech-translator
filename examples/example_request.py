# importing the requests library 
import requests 

# HOST = 'http://ec2-35-180-2-236.eu-west-3.compute.amazonaws.com'
HOST = 'http://localhost'

# defining the api-endpoint, change localhost to real url if necessary
API_ENDPOINT_EN2FR = HOST+":8080/en2fr"
API_ENDPOINT_FR2EN = HOST+":8080/fr2en"

# data to be sent to api 
data_en = {'text2translate': 'The Polish nobility enjoyed many rights that were not available to the noble classes of other countries and, typically, each new monarch conceded them further privileges. Those privileges became the basis of the Golden Liberty in the Polish–Lithuanian Commonwealth. Despite having a king, Poland was called the nobility\'s Commonwealth because the king was elected by all interested members of hereditary nobility and Poland was considered to be the property of this class, not of the king or the ruling dynasty. This state of affairs grew up in part because of the extinction of the male-line descendants of the old royal dynasty (first the Piasts, then the Jagiellons), and the selection by the nobility of the Polish king from among the dynasty\'s female-line descendants.'} 
# data_fr = {'text2translate': 'La noblesse polonaise jouissait de nombreux droits auxquels les nobles d\'autres pays n\'avaient pas droit et, en règle générale, chaque nouveau monarque concédait d\'autres privilèges qui devinrent la base de la Liberté d\'or dans le Commonwealth polonais et lituanien. Bien qu\'ayant un roi, la Pologne a été appelée Commonwealth de la noblesse parce que le roi était élu par tous les membres intéressés de la noblesse héréditaire et que la Pologne était considérée comme la propriété de cette classe, et non du roi ou de la dynastie au pouvoir. Cet état de choses s\'est développé en partie à cause de l\'extinction des descendants masculins de l\'ancienne dynastie royale (d\'abord les Piasts, puis les Jagiellons), et par la noblesse du roi polonais parmi les descendants de la dynastie.'} 
data_fr = {'text2translate': 'La maison est verte'} 

# sending post request and saving response as response object 
r_en2fr = requests.post(url = API_ENDPOINT_EN2FR, data = data_en) 
print('----- EN2FR -----')
print('API endpoint EN2FR: {}'.format(API_ENDPOINT_EN2FR))
print(r_en2fr.text) 
print('-----------------')

r_fr2en = requests.post(url = API_ENDPOINT_FR2EN, data = data_fr) 
print('----- FR2EN -----')
print('API endpoint FR2EN: {}'.format(API_ENDPOINT_FR2EN))
print(r_fr2en.text) 
print('-----------------')
