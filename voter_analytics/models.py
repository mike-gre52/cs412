from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    Rerpresents one voter from the Newton Voter data set
    '''
    first_name = models.TextField()
    last_name = models.TextField()
    address_street_number = models.IntegerField()
    address_street_name = models.TextField()
    address_apartment_number = models.TextField()
    address_zipcode = models.IntegerField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party = models.TextField()
    precinct_number = models.TextField()
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.party}, {self.party})'

def string_to_bool(s: str):
        if s.lower() == "true":
            return True
        else: 
            return False

def load_data():
    '''Function to load voter data records from CSV file into Django model instances.'''
	
    filename = '/Users/mikegreene/Developer/django/data/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            result = Voter(
                first_name=fields[2],
                last_name=fields[1],
                address_street_number = fields[3],
                address_street_name = fields[4],
                address_apartment_number = fields[5],      
                address_zipcode = fields[6],
                date_of_birth = fields[7],
                date_of_registration = fields[8],
                party = fields[9],
                precinct_number = fields[10],
                v20state = string_to_bool(fields[11]),
                v21town = string_to_bool(fields[12]),
                v21primary = string_to_bool(fields[13]),
                v22general = string_to_bool(fields[14]),
                v23town = string_to_bool(fields[15]),
                voter_score = fields[16],
                )
        
            result.save() # commit to database
            #print(f'Created result: {result}')
            
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Results.')