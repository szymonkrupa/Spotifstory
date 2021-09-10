import spotipy.util as util

#Authorization
username = '-user-name'
client_id ='-your-client-id'
client_secret = '-you-secret-client-code'
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played'

def get_token():
    token = util.prompt_for_user_token(username=username, 
                                   scope=scope, 
                                   client_id=client_id,   
                                   client_secret=client_secret,     
                                   redirect_uri=redirect_uri)
    
    return token