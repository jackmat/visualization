#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:41:02 2023

@author: carlessansfuentes
"""

import streamlit as st

# Define some code
code = '''
def hello_world():
    print("Hello, World!")
    
hello_world()
'''

# Display the code in the Streamlit app
st.code(code, language='python')