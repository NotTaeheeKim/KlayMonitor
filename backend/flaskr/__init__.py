import os
# from web3py_ext import extend
# from web3 import AsyncWeb3, AsyncHTTPProvider

from flask import Flask, render_template, request, redirect
from web3 import Web3

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import json

from flask_httpauth import HTTPBasicAuth
import bcrypt
import time

auth = HTTPBasicAuth()
@auth.verify_password
def verify_password(username,password):
    if username in users:
        passwordbytes = password.encode("utf-8")
        passwordsalt = usersalts.get(username)
        return users.get(username) == bcrypt.hashpw(passwordbytes,passwordsalt)
    return False

# ====== HARDCODED TEST DATA ======

user = "User"
pw = "123"

pwsalt = bcrypt.gensalt()
pwbytes = pw.encode("utf-8")
pwhash = bcrypt.hashpw(pwbytes,pwsalt)


users = {user:pwhash}
usersalts = {user:pwsalt}

# ====== HARDCODED TEST DATA ======



def create_app(test_config=None):

    app = Flask(__name__)

    # # create and configure the app
    # app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello


    @app.route('/testpage')
    @auth.login_required
    def testRender():
        return render_template("test.html")
    
    @app.route('/home')
    def homeRender():
        return render_template("home.html")
    
    @app.route("/")
    def redirectToHome():
        return redirect("/home")

    @app.route('/login')
    def loginRender():
        return render_template("login.html")

    @app.route('/register')
    def registerRender():
        return render_template("register.html")

    @app.route('/profile')
    def profileRender():
        return render_template("profile.html")

    @app.route('/index')
    def indexRender():
        return render_template("index.html")
    
    @app.route('/table')
    def tableRender():
        # Obtain address as parameter
        targetAddress = str(request.args.get("address"))
        # Define transport and url endpoint
        transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/74689/klaytrackertest/v0.1")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        queryString = f"""query{{
            transfers(
                where: {{
                    or: [
                        {{ from: "{targetAddress}" }},
                        {{ to: "{targetAddress}" }}
                    ]
                }}
            ){{
                transactionHash
                from
                to
                value
                blockTimestamp
                # other desired fields
            }}
        }}"""
        print(targetAddress)
    
        # Provide a GraphQL query
        query = gql(
            queryString
        ) 

        # Execute the query on the transport
        try:    
            result = client.execute(query)
        except:
            result = client.execute(gql("""query{
                transfers{
                    transactionHash
                    from
                    to
                    value
                    blockTimestamp
                    # other desired fields
                }
            }
            """)
            )


   
        for element in result["transfers"]:  
            # Get the local time from the timestamp
            time_object = time.localtime(int(element["blockTimestamp"]))

            # Format the time using strftime
            formatted_time = time.strftime("%H:%M:%S %d/%m/%Y", time_object)
            element["blockTimestamp"]=formatted_time


        return render_template("table.html",data=result["transfers"])

    @app.route('/fetchBalance')
    def retrieve():
        print(bcrypt.gensalt())
        balance = 0


        try:
            address = Web3.to_checksum_address(request.args.get("address"))

            # w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://public-en-baobab.klaytn.net', request_kwargs={'ssl':False}))
            w3 = Web3(Web3.HTTPProvider('https://ethereum-rpc.publicnode.com'))
            result = w3.eth.get_balance(address)
            print(result)
            balance = result 
        except Exception as e:
            print(f"Error: {e}")
            return "Error Occurred"

        return balance

    @app.route('/test2')
    def fetch():
        # read database
        return {"1":30, "2": 40, "3":20, "4": 60, "5":70, "6": 50}

    @app.route('/insertTest')
    def insertTable():
        result = ""
        return result
    return app