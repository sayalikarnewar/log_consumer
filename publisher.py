import pika
import time
import json
       

class logger():
    flag = [False]
    def __init__(self):
        #'''create the connection '''
        self.flag[0] = True
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672', '/', pika.PlainCredentials('guest', 'guest')))
            self.channel = connection.channel()
            #'''declare the exchange'''
            try:
                self.channel.exchange_declare(exchange="logger", exchange_type="fanout")
            except:
                self.flag.append("FAILURE: exchange declare failed.")
                self.flag[0] = False
                
        except:
            self.flag.append("FAILURE: connection establishment failed. check init()")
            self.flag[0] = False
       

    #logger function 
    def log(self, time_stamp, service_name, tag, message):   
        if self.flag[0] == True:
            try:
                body = {
                            'time_stamp' : time.time(), 
                            'service_name' : service_name,
                            'tag' : tag,
                            'message' : message
                        }
            except:
                self.flag[0] = False
                self.flag.append("FAILURE: error in body. time()/spelling mistake")
            

            #check if dumps!
            if self.flag[0]==True:
                try:
                    self.json_object = json.dumps(body)
                except:
                    self.flag[0] = False
                    self.flag.append("FAILURE: error in json object or json dumps")
                  

                #check if or not publihed
                if self.flag[0]==True:
                    try:
                        self.channel.basic_publish(exchange='logger', routing_key='', body=self.json_object)
                        
                    except:
                        self.flag[0] = False
                        self.flag.append("FAILURE: error in basic publish")
                    else:
                        self.flag.append('Successfully published')
                    


    # Calling destructor 
    def __del__(self): 
        try:
            self.channel.close()
        except:
            self.flag[0] = False
            self.flag.append("FAILURE: destructor failed")