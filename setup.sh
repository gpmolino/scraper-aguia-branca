mkdir -p ~/.streamlit/

echo " [general]
email = 'botocudos.data.science@gmail.com'
" > ~/.streamlit/credentials.toml

echo "[server]
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml

