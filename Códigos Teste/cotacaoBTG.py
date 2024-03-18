from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
# Inicializar o WebDriver do Chrome
driver = webdriver.Chrome(service=service, options=options)

# Abrir o site de login
driver.get("https://access.btgpactualdigital.com/login/externo")

# Localizar os campos de entrada (geralmente por meio de seus IDs, nomes ou outros seletotes)
username_field = driver.find_element("name","login")
password_field = driver.find_element("name","password")

# Preencher os campos de entrada
username_field.send_keys("seu_nome_de_usuario")
password_field.send_keys("sua_senha")

# Enviar o formulário de login
password_field.send_keys(Keys.RETURN)

# Aguardar um pouco para que o processo de login seja concluído
time.sleep(5)

# Fechar o navegador
driver.quit()
