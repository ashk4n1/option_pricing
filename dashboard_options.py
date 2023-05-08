#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import scipy.stats as ss
import pandas as pd
from PIL import Image
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from option_price import *

st.set_page_config(page_title="European Option Pricing using Black-Scholes Model")
sidebar_title = st.sidebar.header("Black-Scholes Parameters")

OPTION_PRICING_MODEL = ['Black scholes']
pricing_method = st.sidebar.radio('Please select option pricing method',
                                  options=[model for model in OPTION_PRICING_MODEL])

if pricing_method == 'Black scholes':

    payoff = st.sidebar.selectbox("Option Type", ["Call", "Put"])
    S = st.sidebar.number_input("Spot", min_value=1.00, step=0.10, value=30.00)
    K = st.sidebar.number_input("Strike Price", min_value=1.00, step=0.10, value=40.00)
    sigma = st.sidebar.slider("Volatility", 0.0, 2.0, (0.43))
    days_to_expiry = st.sidebar.number_input("Time to Expiry Date (in days)", min_value=1, step=1, value=220)
    r = st.sidebar.number_input("Risk-Free Rate", min_value=0.000, max_value=1.000, step=0.001, value=0.13)

    T = days_to_expiry / 365

    spot_prices = [s for s in range(0, int(S) + 101)]

    prices = [BlackScholes(payoff, s, K, T, r, sigma) for s in spot_prices]
    deltas = [delta(payoff, s, K, T, r, sigma) for s in spot_prices]
    gammas = [gamma(s, K, T, r, sigma) for s in spot_prices]
    vegas = [vega(s, K, T, r, sigma) for s in spot_prices]
    rhos = [rho(payoff, s, K, T, r, sigma) for s in spot_prices]
    thetas = [theta(payoff, s, K, T, r, sigma) for s in spot_prices]

    sns.set_style("whitegrid")

    st.markdown("<h1 align='center'>European Option Pricing</h1>", unsafe_allow_html=True)
    st.header("")
    st.write(
        'Under the Black-Scholes (BS) model, the most straightforward method to price a vanilla european option is to use the BS analytical formula.')
    st.write(' Call option (C) and put option (P) prices are calculated using the following formulas:')
    st.latex('C(t,T,S_t,K,r,\sigma) = S_t N(d_1) - K e^{-r(T-t)} N(d_2)')
    st.latex('P(t,T,S_t,K,r,\sigma) = K e^{-r(T-t)} N(-d_2) - S_t N(-d_1)')
    st.markdown('Or under Put-Call parity:')
    st.latex('Call - Put = S_0 - K e^{-rT}')

    st.write(' Where $d_1$ and $d_2$ are given by: ')
    st.latex(
        r'd_1 = \frac{1}{\sigma \sqrt{T-t}} \biggl[ \log \biggl( \frac{S_t}{K} \biggr) + \biggl(r + \frac{\sigma^2}{2} \biggr) (T-t) \biggr]')
    st.latex('d_2 = d_1 - \sigma \sqrt{T-t}')

    st.header("")
    # style
    th_props = [
        ('font-size', '14px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#6d6d6d'),
        ('background-color', '#f7ffff')
    ]

    td_props = [
        ('font-size', '20px')
    ]

    styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
    ]

    valores = np.array([[
        round(delta(payoff, S, K, T, r, sigma), 3),
        round(gamma(S, K, T, r, sigma), 3),
        round(vega(S, K, T, r, sigma), 3),
        round(rho(payoff, S, K, T, r, sigma), 3),
        round(theta(payoff, S, K, T, r, sigma), 3)]])

    temp1 = pd.DataFrame(
        np.array([[round(BlackScholes("Call", S, K, T, r, sigma), 3),
                   round(BlackScholes("Put", S, K, T, r, sigma), 3)]]),
        columns=(['Call', 'Put']), index=['Values']).T

    temp2 = pd.DataFrame(
        valores,
        columns=(['Delta', 'Gamma', 'Vega', 'Rho', 'Theta']), index=['Values']).T

    df = temp1.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles).format(precision=3)
    df2 = temp2.style.set_properties(**{'text-align': 'left'}).set_table_styles(styles).format(precision=3)

    st.table(df)
    st.table(df2)

    st.header("")

    st.write('### Visualization')
    visualize = st.button(f'Plot Greeks')

    if visualize:
        two_subplot_fig = plt.figure()
        plt.subplot(231)
        plt.plot(spot_prices, prices, color='black', marker='.')
        plt.ylabel("Option Price")
        plt.xlabel("Spot")
        plt.subplots_adjust(bottom=-0.15)

        plt.subplot(232)
        plt.plot(spot_prices, deltas, color='black', marker='.')
        plt.subplots_adjust(bottom=- 0.15)
        plt.ylabel("Delta")
        plt.xlabel("Spot")

        plt.subplot(233)
        plt.plot(spot_prices, gammas, color='black', marker='.')
        plt.subplots_adjust(bottom=- 0.15)
        plt.ylabel("Gamma")
        plt.xlabel("Spot")

        plt.subplot(234)
        plt.plot(spot_prices, thetas, color='black', marker='.')
        plt.subplots_adjust(bottom=- 0.15)
        plt.ylabel("Theta")
        plt.xlabel("Spot")

        plt.subplot(235)
        plt.plot(spot_prices, vegas, color='black', marker='.')
        plt.subplots_adjust(bottom=- 0.15)
        plt.ylabel("Vega")
        plt.xlabel("Spot")

        plt.subplot(236)
        plt.plot(spot_prices, rhos, color='black', marker='.')
        plt.subplots_adjust(bottom=- 0.15)
        plt.ylabel("Rho")
        plt.xlabel("Spot")

        st.pyplot(two_subplot_fig)

    st.write('### Sensitivies')
    greeks = st.button(f'Greeks formula')

    if greeks:
        st.write(
            'A way of describing the reaction of option prices to a change in the underlying parameter is to consider their sensitivities, which are also called the Greeks.')
        st.write('The most common Greeks formula is given by:')
        st.write('**Delta** for a Call Option')
        st.latex(r'\Delta := \frac{\partial V}{\partial S} = e^{-(T-t)}N(d_1).')
        st.write('**Delta** for a  Put Option')
        st.latex(r'\Delta := \frac{\partial V}{\partial S} = e^{-(T-t)}( N(d_1) - 1).')

        st.write('**Gamma** for a Call/Put Option')
        st.latex(r'\Gamma := \frac{\partial^2 V}{\partial S^2} = \frac{e^{-(T-t)} N\'(d_1)}{\sigma S \sqrt{T-t}}.')

        st.write('**Vega** for a Call Option')
        st.latex(r'\mathcal{V} := \frac{\partial V}{\partial \sigma} = S(T-t) e^{-(T-t)} N\'(d_1).')

        st.write('**Rho** for a Call Option')
        st.latex(r'\rho := \frac{\partial V}{\partial r} = K(T-t)e^{-r(T-t)} N(d_2).')
        st.write('**Rho** for a Put Option')
        st.latex(r'\rho := \frac{\partial V}{\partial r} = -K(T-t)e^{-r(T-t)} N(-d_2).')

        st.write('**Theta** for a Call Option')
        st.latex(
            r'\Theta := \frac{\partial V}{\partial t} = -\frac{\sigma S e^{-(T-t)} N\'(d_1)}{2 \sqrt{T-t}} - rKe^{-r(T-t)} N(d_2).')
        st.write('**Theta** for a Put Option')
        st.latex(
            r'\Theta := \frac{\partial V}{\partial t} = -\frac{\sigma S e^{-(T-t)} N\'(-d_1)}{2 \sqrt{T-t}} + rKe^{-r(T-t)} N(-d_2).')
