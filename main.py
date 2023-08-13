import streamlit_authenticator as stauth
from utils import *

config = update_config()

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')
print(name, authentication_status, username)

if authentication_status:
    st.sidebar.subheader(f'Welcome {username}')
    authenticator.logout('Logout', 'sidebar')
    st.subheader('Home page')
    st.markdown(
        """
        ---
        Created with ❤️ by reflexive.ai

        """
    )
    print(f"current st.session_state:{st.session_state}")
    st.write(st.session_state)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# Creating a password reset widget
    if authentication_status:
        try:
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    # Creating a new user registration widget
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
            print('User registered successfully')
            print(f"updated full config:{config}")
            print(f"updated credential:{config['credentials']}")
            # at this point, config has been updated by authenticate.py, need to update the yaml file
            add_user(config['credentials'])
    except Exception as e:
        st.error(e)

# need to force the logout otherwise the credentials are kept in memory / cache

