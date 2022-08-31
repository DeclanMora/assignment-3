#Importing required libraries
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

#Load in the .env file
load_dotenv()
 
#Defining and connecting the Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
 
#Create a function to load the contract into the app
@st.cache(allow_output_mutation=True)
def load_contract():
    with open(Path(r'C:\Users\User\OneDrive\Documents\Repos\Assignment\assignment 3\BTScoin\contract\compiled\bts_abi.json')) as f:
        bts_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    contract = w3.eth.contract(
        address=contract_address,
        abi= bts_abi
    )
    return contract

#Setting a variable 'contract' to the smart contract loaded in with Web3
token = load_contract()

#Create welcome section for the app
st.image(r'C:\Users\User\OneDrive\Documents\Repos\Assignment\assignment 3\resources\BTSlogo.jpg')
st.title('Welcome aboard Born-To-Survive! Are you ready to survive?')

#Set up accounts via Web3 connection
accounts = w3.eth.accounts
address = st.sidebar.selectbox('Select Ethereum Account', options = accounts)


st.header('What would you like to do today?')

#Ideally, we would want the following 3 buttons to navigate to a different page for the app
#st.button('Purchase Product')
#st.button('Purchase BornToSurvive Tokens')
#st.button('Return/Exchanges')
 
#Creating the purchase order button for Streamlit app
st.header('BornToSurvive Token Purchase')

#Create a slider widget allowing customers to select the quantity of tokens they want to purchase
token_quantity = st.slider('Select how many BornToSurvive Tokens you want to purchase (per transaction limits: min. is 1; max is 10.):', 
                            min_value = 1, max_value = 10)

if token_quantity == 1:
    st.write('You are buying', token_quantity, 'BornToSurvive Token.')
else:
    st.write('You are buying', token_quantity, 'BornToSurvive Tokens.')

#Create button to confirm purchase of the tokens
if st.button('Purchase BornToSurvive Tokens'):
    tx_hash = token.functions.purchase(token_quantity).transact({'from': address})
    st.write('Tokens Purchased!')
    st.balloons()

#Create section for customer to see their token balance
if st.button('Show BornToSurvive Token Balance Snapshot'):
    token_balance_snapshot = token_quantity
    st.write('Your BornToSurvive Token Balance is', token_balance_snapshot, 'BornToSurvive Tokens.')

#Create section for customer to purchase store product
st.header('Product Purchase Order')
st.write('Please select your purchase options below:')

#Create a selection box of the product that the customer wants to purchase
st.selectbox('Choose your Faction', ['Amarr', 'Caldari', 'Gallente', 'MinMatar'])

#Create a list of product options
product_options = ['Base Scout - 1BTS', 'Base Cruiser - 2BTS', 'Base Fighter - 3BTS', 'Base Frigate - 4BTS']

#Set variables to the product selection and quantity to calculate the total cost
selection = st.selectbox('Select Product Unit', product_options)
quantity = st.number_input('Quantity - Please use whole numbers only.')

#Create a function to show the customer the total cost of their product purchase
@st.cache(suppress_st_warning=True)
def get_total_cost(selection, quantity):
    price = 0
    if selection == 'Base Scout - 1BTS':
        price = 1
        total_cost = price * quantity
        st.write('The total cost for your order is BTS', round(total_cost, 2), '.')
    elif selection == 'Base Cruiser - 2BTS':
        price = 2
        total_cost = price * quantity
        st.write('The total cost for your order is BTS', round(total_cost, 2), '.')
    elif selection == 'Base Fighter - 3BTS':
        price = 3
        total_cost = price * quantity
        st.write('The total costs for your order is BTS', round(total_cost, 2), '.')
    elif selection == 'Base Frigate - 4BTS':
        price = 4
        total_cost = price * quantity
        st.write('The total cost for your order is BTS', round(total_cost, 2), '.')

#Create button to display total cost of product purchase to customer
if st.button('Show Total Cost'):
    get_total_cost(selection, quantity)


#This button is still in process, to confirm the store product purchase from the store
# confirm_purchase = st.button('Confirm Purchase')
# if confirm_purchase:
#     #Put in order for the product
#     st.write("Purchase confirmed.")