import csv
USERS_CSV = 'users.csv'
RECORDINGS_CSV = 'recordings.csv'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])
# Function to check if user exists
def user_exists(username):
    with open(USERS_CSV, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True
    return False

# Checks so file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS