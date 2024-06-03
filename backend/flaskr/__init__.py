import os
# from web3py_ext import extend
# from web3 import AsyncWeb3, AsyncHTTPProvider

from flask import Flask, render_template, request
from web3 import Web3

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import json

from flask_httpauth import HTTPBasicAuth
import bcrypt

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


    @app.route('/')
    @auth.login_required
    def testRender():
        return render_template("test.html")
    
    @app.route('/home')
    def homeRender():
        return render_template("home.html")

    @app.route('/login')
    @auth.login_required
    def loginRender():
        return render_template("login.html")

    @app.route('/register')
    @auth.login_required
    def registerRender():
        return render_template("register.html")

    @app.route('/test')
    def retrieve():
        print(bcrypt.gensalt())

        klaytnBalance = "testing"
        balance = 0
        privateKey = "0xf0b695328ee59cec0bbf2f2efd309423c8e1cb427f82ac0ea3552d30c63f6f68"
        address = Web3.to_checksum_address("0x7cd2bb56142bf8ab104c8c1eddef9b1c32b04979")

        # w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider('https://public-en-baobab.klaytn.net', request_kwargs={'ssl':False}))
        w3 = Web3(Web3.HTTPProvider('https://public-en-baobab.klaytn.net'))

        try:
            result = w3.eth.get_balance(address)
            print(result)
            balance = result / 1000000000000000000
        except Exception as e:
            print(f"Error: {e}")

        return {"address":address, "balance": balance}

    @app.route('/test2')
    def fetch():
        # read database
        return {"1":30, "2": 40, "3":20, "4": 60, "5":70, "6": 50}

    @app.route('/testSubquery')
    def testquery():
        # Obtain address as parameter
        targetAddress = request.args.get("address")
        # Define transport and url endpoint
        transport = AIOHTTPTransport(url="https://api.studio.thegraph.com/query/74689/klaytrackertest/v0.1")

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Provide a GraphQL query
        query = gql(
            """
            query{
                transfers{
                    id
                    from
                    to
                    value
                    # other desired fields
                }
            }
            """
        )

        # Execute the query on the transport
        result = client.execute(query)


        #Calculate
        history = {}
        balance = 0
        count = 0
        for element in result["transfers"]:
            if element["from"] == targetAddress:
                balance-=int(element["value"])
                history.update({str(count):str(balance)})
                count +=1

            elif element["to"] == targetAddress:
                balance+=int(element["value"])
                history.update({str(count):str(balance)})
                count +=1

        # test with address: 0x28c6c06298d514db089934071355e5743bf21d60
        print(history)
        history = json.dumps(history)
        return history
    return app