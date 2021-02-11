try:
    import pika
    import json
    import pymongo
    import smtplib, ssl
except:
    print("FAILURE: import libraries")
else:
    print("SUCCESS: imported libraries")        

try:    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672', '/', pika.PlainCredentials('guest', 'guest')))
    channel = connection.channel()
except:
    print("FAILURE: connection establishment failed.")
else:
    print("SUCCESS: connection success.")
                
#declare the exchange
try:
    channel.exchange_declare(exchange='logger', exchange_type="fanout")
except:
    print("FAILURE: exchange declare failed.")    
else:
    print("SUCCESS: exchange declared success")   

#declare the queue
try:
    result = channel.queue_declare(queue='')
except:
    print("FAILURE: queue declare failed.")    
else:
    print("SUCCESS: queue declared success")    

#'''bind the queue with the exchange'''
try:
    channel.queue_bind(exchange='logger', queue=result.method.queue)
except:
    print("FAILURE: queue bind failed.")    
else:
    print("SUCCESS: queue bind success")

#'''pymongo database connection'''
try:
    db_object = pymongo.MongoClient("mongodb://localhost:27017").folloDB.logger  #database and collection name
except:
    print("FAILURE: db connection failed")
else:
    print("SUCCESS: db connection successful")    

#'''receiver function'''
def receiver_function(ch, method, properties,body):
    try:
        message = json.loads(body)
        print("received logs: ",message)
        message1 = json.dumps(message)
    except:
        print("FAILURE: json dumps.")    
    else:
        print("SUCCESS: json dumps")  

         
    db_object.insert_one(message).inserted_id
    if message["tag"] == "CRITICAL" or "WARNING" or "ERROR":

        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        receievr_email = ["sayali@follo.care"]
        sender_email = "sayalitest123@gmail.com"
        password = "angellist123"
        msg = """\

       """ + message1

        
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.starttls() # Secure the connection context=context
            server.login(sender_email, password)
            server.sendmail(sender_email, receievr_email, msg)
            print("email sent to :", receievr_email)
        except:
            print("FAILURE: SMTP server")
        else:
            print("SUCCESS: SMTP server success")    
        finally:
            server.quit() 
#consume the message from the queue'''
try:
    channel.basic_consume(queue=result.method.queue, on_message_callback=receiver_function, auto_ack=True)
    channel.start_consuming()
except:
    print("FAILURE: basic_consume()/start_consuming()")
else:
    print("SUCCESS: message consumed")    
