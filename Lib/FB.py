import ConfigParser


############LOADING CONFIG FILES ##################
config = ConfigParser.ConfigParser()
config.read('Lib/API.cfg')
Token = config.get("Facebook", 'access_token')

graph = facebook.GraphAPI(access_token=Token)
def main(event):
    print ("facebook")
