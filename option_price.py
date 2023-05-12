#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import norm
import streamlit as st

def BlackScholes(payoff='Call', S=200., K=200., T=1., r=0.1, sigma=0.25 ):
    """ Black Scholes analytical formula for pricing european options:
        payoff: Call or Put.
        S: Initial stock/index level.
        K: Strike price.
        T: Maturity (in year fractions).  
        r: Constant risk-free rate.
        sigma: Volatility. """
   
    d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S/K) + (r - sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    try:
        if payoff=="Call":
            return S * norm.cdf( d1 ) - K * np.exp(-r * T) * norm.cdf(   d2 )
        elif payoff=="Put":
            return K * np.exp(-r * T) * norm.cdf( -d2 ) - S * norm.cdf( -d1 )
    except:  
            raise ValueError("Invalid type. Set 'call' or 'put'")
            st.sidebar.error("Please confirm all option parameters!")
            
def delta (payoff='call', S=200., K=200., T=1., r=0.1, sigma=0.25 ):
    """ BS delta: 
    Delta measures the rate of change of the option to changes in the underlying asset. """

    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        if payoff == "Call":
            delta = norm.cdf(d1)
        elif payoff == "Put":
            delta = -norm.cdf(-d1)

        return delta
    except:
        st.sidebar.error("Please confirm all parameters!")            
       
def gamma (S=200., K=200., T=1., r=0.1, sigma=0.25):
    """ BS gamma: 
    Gamma measures the rate of change of Delta to changes in the underlying asset.. """

    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        gamma = norm.pdf(d1)/ (S * sigma * np.sqrt(T))
        return gamma
    except:
        st.sidebar.error("Please confirm all parameters!")
        
        
def vega(S=200., K=200., T=1., r=0.1, sigma=0.25):
    """ BS vega: 
    Vega measures the rate of change of the price with respect to the volatility """
    
    d1 = (np.log(S/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    try:
        vega = 0.01 * S * np.sqrt(T) * norm.pdf(d1)
        return vega
    except:
        st.sidebar.error("Please confirm all parameters!")
        
def theta(payoff='call', S=200., K=200., T=1., r=0.1, sigma=0.25):
    """ BS theta: 
    Theta measures the sensitivity of the option to the passage of time. """

    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        if payoff == "Call":
            theta = - ((S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) - r * K * np.exp(-r*T) * norm.cdf(d2)

        elif payoff == "Put":
            theta = - ((S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) + r * K * np.exp(-r*T) * norm.cdf(-d2)
        return theta/365
    except:
        st.sidebar.error("Please confirm all parameters!")
    
def rho(payoff='call', S=200., K=200., T=1., r=0.1, sigma=0.25):
    """ BS theta: 
    Derivative of the price with respect to the time. """
    d1 = (np.log(S/K) + (r + sigma**2/2)* T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    try:
        if payoff == "Call":
            rho =  0.01 * K * T * np.exp(-r*T) * norm.cdf(d2)
        elif payoff == "Put":
            rho = 0.01 * -K * T * np.exp(-r*T) * norm.cdf(-d2)
        return rho
    except:
        st.sidebar.error("Please confirm all parameters!")
