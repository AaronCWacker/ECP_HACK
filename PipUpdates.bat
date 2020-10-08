rem Get latest code
git pull

rem Start updating packages
python -m pip install --upgrade pip --user

python -m pip install anytree --upgrade --user
python -m pip install bokeh --upgrade --user
python -m pip install beautifulsoup4 --upgrade --user
python -m pip install CookieJar --upgrade --user
python -m pip install cx_Oracle --upgrade --user
python -m pip install dbf --upgrade --user
python -m pip install django --upgrade --user
python -m pip install detect --upgrade --user
python -m pip install detect_delimiter --upgrade --user
python -m pip install dbutils --upgrade --user
python -m pip install easytextract --upgrade --user
python -m pip install flask --upgrade --user
python -m pip install flask_restful --upgrade --user
python -m pip install flask-utils --upgrade --user
python -m pip install -U flask_cors --user
python -m pip install gviz_api --upgrade --user
python -m pip install gensim --upgrade --user
python -m pip install holoviews --upgrade --user
python -m pip install html2text --upgrade --user
python -m pip install hl7 --upgrade --user
python -m pip install hl7apy --upgrade --user
python -m pip install keras --upgrade --user
python -m pip install json2html --upgrade --user
python -m pip install matplotlib --upgrade --user
python -m pip install mechanize --upgrade --user
rem Cannot find ntlm package any longer
rem pip install ntlm --upgrade --user
python -m pip install ntlm-auth --upgrade --user
python -m pip install numpy --upgrade --user
python -m pip install nltk --upgrade --user
python -m pip install pandas --upgrade --user
python -m pip install plotly --upgrade --user
python -m pip install python-ntlm --upgrade --user
python -m pip install pypdf2 --upgrade --user
python -m pip install pipenv --upgrade --user
python -m pip install requests --upgrade --user
python -m pip install requests_ntlm --upgrade --user
python -m pip install seaborn --upgrade --user
python -m pip install sharepoint --upgrade --user
python -m pip install sharepy --upgrade --user
python -m pip install tensorflow --upgrade --user
python -m pip install theano --upgrade --user
python -m pip install twilio --upgrade --user
python -m pip install utils --upgrade --user
python -m pip install xlrd --upgrade --user
python -m pip install py2neo --upgrade --user
python -m pip install psutil --upgrade --user

rem in OCM-ML dir, which needs to be in the dir for installation
rem Needs to be run first before pip installing python-ldap
rem Following works on Dev
python -m pip install .\python_ldap-3.2.0-cp36-cp36m-win_amd64.whl
rem Following works on Stage
python -m pip install .\python_ldap-3.2.0-cp37-cp37m-win_amd64.whl
rem latest
python -m pip install .\python_ldap-3.2.0-cp38-cp38-win_amd64.whl

python -m pip install python-ldap --upgrade --user
python -m pip install requests_oauthlib --upgrade --user

rem Added 3 more libs for epal reader
python -m pip install lxml --upgrade --user
python -m pip install io --upgrade --user
python -m pip install unidecode --upgrade --user

python -m pip install graphene
python -m pip install flask_swagger --upgrade
python -m pip install flask_swagger_ui --upgrade
python -m pip install bs4 --upgrade
python -m pip install waitress --upgrade

python -m pip install pdfkit --upgrade
python -m pip install Jinja2 --upgrade

rem Added 6 more libs for Bokeh
rem https://docs.bokeh.org/en/latest/docs/installation.html
python -m pip install packaging --update
python -m pip install pillow --update
python -m pip install python-dateutil --update
python -m pip install PyYAML --update
python -m pip install six --update
python -m pip install tornado --update

python -m pip install openpyxl --upgrade --user
rem pip install git+https://github.optum.com/clinical/ocm-ml-common-lib.git --upgrade
python -m pip install .\ocm_ml_common-2019.11.18-py2.py3-none-any.whl

conda install  -y m2w64-toolchain

rem Leave as last line in *.Bat file
conda install -y anaconda seaborn

echo You may have to install an older version of tensorflow on windows servers
echo    python -m pip install --upgrade tensorflow==1.15 --user

python -m pip install pycurl
python -m pip install fastapi
echo ensure these are in your path for uvicorn install
echo ...\Anaconda3;
echo ...\Anaconda3\Scripts;
echo ...\Anaconda3\Library\bin
python -m pip install uvicorn
rem pip install CORSMiddleware
python -m pip install jinja2
python -m pip install pyTigerGraph
python -m pip install aiofiles
python -m pip install python-multipart
python -m pip install pyjwt
python -m pip install passlib[bcrypt]
python -m pip install dataclasses
python -m pip install dataclasses-json

rem Screen updates
python -m pip install PyQt5
python -m pip install pyautogui
python -m pip install playsound
python -m pip install colorlog
