import Dependencies as dp


dp.load_dotenv()

TARGET_SHEET = dp.os.getenv('TARGET_SHEET')
PAGE_URL = dp.os.getenv('PAGE_URL')
DOWNLOAD_DIR = dp.os.getenv('DOWNLOAD_DIR')


# ABRIR UMA PÁGINA CHROME
def create_driver():
    driver = dp.webdriver.Chrome()
    return driver


# ACESSAR SISTEMA
def access_system(driver, user, password):
    driver.get(PAGE_URL)
    driver.maximize_window()

    # USUARIO
    user_field = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, 'form:txtDesUsuario_c')))
    user_field.send_keys(user)

    # SENHA
    password_field = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, 'form:txtDesSenha_c')))
    password_field.send_keys(password)

    # CLICAR PARA ENTRAR
    enter_button = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.XPATH, "//span[@class='ui-button-text ui-c']")))
    enter_button.click()

    # CONSULTAS DINAMICAS
    dinQueries_button = driver.find_elements(dp.By.XPATH, "//h3[@class='ui-accordion-header ui-helper-reset ui-state-default ui-corner-all']")
    dinQueries_button[9].click()

    # CONSULTA SERVIDORES
    servQueries_button = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.LINK_TEXT, "Consulta Servidores")))
    servQueries_button.click()


# EXTRAIR RELATÓRIO DE ATIVOS
def extract_report(driver, filter):
    # LIMPAR TUDO
    try:
        dp.time.sleep(1)
        clear_all = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, "form:btnLimpar")))
        clear_all.click()
        print("Botão de limpar tudo clicado.")
        dp.time.sleep(2)
    except Exception as error:
        print("Erro ao tentar clicar em 'LIMPAR TUDO'")
        dp.pya.alert("Erro ao tentar clicar em 'LIMPAR TUDO'")
    
    # CAMPO SITUAÇÃO
    if filter == 'ATIVOS':
        try:
            situation_field = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, 'form:lovCreator_14834_txt_cod')))
            situation_field.send_keys('0') # SITUAÇÃO ATIVOS
            print("Situação dos colaboradores aplicada.")
            dp.pya.press('tab')
            dp.time.sleep(2)
        except Exception as error:
            print("Erro ao tentar inserir 'SITUAÇÃO'")
            dp.pya.alert("Erro ao tentar inserir 'SITUAÇÃO'")
    
    # CAMPO VÍNCULO
    try:
        relation_field = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, 'form:lovCreator_14836_txt_cod')))
        relation_field.send_keys('4') # VÍNCULO TERCEIRIZADOS
        print("Vínculo de terceirizados aplicado.")
        dp.pya.press('tab')
        dp.time.sleep(2)
    except Exception as error:
        print("Erro ao tentar inserir 'VÍNCULO'")
        dp.pya.alert("Erro ao tentar inserir 'VÍNCULO'")
        
    # FILTRO
    try:
        dp.time.sleep(1)
        radio_buttons = dp.WebDriverWait(driver, 10).until(dp.EC.presence_of_all_elements_located((dp.By.XPATH, "//span[@class='ui-radiobutton-icon ui-icon ui-icon-blank ui-c']")))
        for index, radio_button in enumerate(radio_buttons):
            if filter == 'ATIVOS':
                if index == 5:
                    radio_button.click()
                    print("Filtro de ativos selecionado com sucesso.")
                    break
            elif filter == 'GERAL':
                if index == 4:
                    radio_button.click()
                    print("Filtro geral selecionado com sucesso.")
                    break
    except Exception as error:
        print("Erro ao tentar inserir 'FILTRO'")
        dp.pya.alert("Erro ao tentar inserir 'FILTRO'")

    # BOTÃO EXECUTAR
    try:
        execute_button = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, "form:btnExecutar")))
        execute_button.click()
        dp.time.sleep(15)
    except Exception as error:
        print("Erro ao tentar clicar no botão 'EXECUTAR'")
        dp.pya.alert("Erro ao tentar clicar no botão 'EXECUTAR'")


# EXPORTAR COMO EXCEL
def export_as_excel(driver):
    # BOTÃO EXPORTAR
    try:
        try:
            export_button = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, "form:btnExportar_menuButton")))
            export_button.click()
        except:
            export_button = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, "form:btnExportar_menuButton")))
            export_button.click()
    except Exception as error:
        print(f"Erro ao tentar clicar no 'Botão de Exportar': {error}")
        dp.pya.alert(f"Erro ao tentar clicar no 'Botão de Exportar'")

    # BOTÃO EXPORTAR
    xlsx_option = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.LINK_TEXT, "Exportar para XLSX")))
    xlsx_option.click()
    dp.time.sleep(5)


# ACESSAR SISTEMA > EXTRAIR RELATÓRIO > EXPORTAR COMO EXCEL
def handle_website_1(driver, user, password, filter):
    access_system(driver, user, password)
    extract_report(driver, filter)
    export_as_excel(driver)
        
      
# # # Opção ainda não desenvolvida        
def handle_website_2():
    pass


# PEGAR O XLSX BAIXADO
def get_downloaded_file(download_dir):
    file_path = None
    timeout = 60
    start_time = dp.time.time()
    
    while dp.time.time() - start_time < timeout:
        files = dp.os.listdir(download_dir)
        if files:
            xlsx_files = [file for file in files if file.endswith('.xlsx')]
            if xlsx_files:
                sorted_xlsx_files = sorted(xlsx_files, key=lambda x: dp.os.path.getmtime(dp.os.path.join(download_dir, x)), reverse=True)
                print(sorted_xlsx_files[0])
                last_file = sorted_xlsx_files[0]
                file_path = dp.os.path.join(download_dir, last_file)
                print(file_path)
                break
        dp.time.sleep(1)
    return file_path


# MANIPULAR XLSX BAIXADO
def handle_worksheet(file_path, filter):
    # PANDAS
    downloaded_sheet = dp.pd.read_excel(file_path, sheet_name='Report')
    sintetic_columns = ['Matrícula','CPF','Nome','E-mail','Dt. Admissão','Função', 'Cod. Setor', 'Setor', 'Convênio']
    sintetic_sheet = downloaded_sheet.loc[:, sintetic_columns]
    
    if filter == 'ATIVOS':
        try:
            target_sheet = downloaded_sheet.copy()
            SHEET_NAME='Ativos_Analítica'
            with dp.pd.ExcelWriter(TARGET_SHEET, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                target_sheet.to_excel(writer, SHEET_NAME, index=False)
                # format_worksheet(TARGET_SHEET, SHEET_NAME)
            print(f'Aba {SHEET_NAME.upper()} sobrescrita com sucesso!')
        except Exception as error:
            print(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
            print(error)
            dp.pya.alert(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
        try:    
            target_sheet = sintetic_sheet.copy()
            SHEET_NAME='Ativos_Sintética'
            with dp.pd.ExcelWriter(TARGET_SHEET, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                target_sheet.to_excel(writer, SHEET_NAME, index=False)
                # format_worksheet(TARGET_SHEET, SHEET_NAME)
            print(f'Aba {SHEET_NAME.upper()} sobrescrita com sucesso!')
        except Exception as error:
            print(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
            print(error)
            dp.pya.alert(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
            
    elif filter == 'GERAL':
        try:
            target_sheet = downloaded_sheet.copy()
            SHEET_NAME='Geral_Analítica'
            with dp.pd.ExcelWriter(TARGET_SHEET, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                target_sheet.to_excel(writer, SHEET_NAME, index=False)
                # format_worksheet(TARGET_SHEET, SHEET_NAME)
            print(f'Aba {SHEET_NAME.upper()} sobrescrita com sucesso!')
        except Exception as error:
            print(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
            print(error)
            dp.pya.alert(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
        
        try:
            target_sheet = sintetic_sheet.copy()
            SHEET_NAME='Geral_Sintética'
            with dp.pd.ExcelWriter(TARGET_SHEET, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                target_sheet.to_excel(writer, SHEET_NAME, index=False)
                # format_worksheet(TARGET_SHEET, SHEET_NAME)
            print(f'Aba {SHEET_NAME.upper()} sobrescrita com sucesso!')
        except Exception as error:
            print(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
            print(error)
            dp.pya.alert(f'Erro ao tentar sobrescrever aba {SHEET_NAME.upper()}')
    
    dp.os.startfile(TARGET_SHEET)
    
    
def format_worksheet(file_path, sheet_name):
    # OPENPYXL
    workbook = dp.load_workbook(file_path)
    worksheet = workbook[sheet_name]
    font = dp.Font(name='Calibri', size=10)
    for row in worksheet.iter_rows():
        for cell in row:
            cell.font = font
    workbook.save(file_path)


# AGUARDAR O TRATAMENTO DA PLANILHA
def wait_handle_worksheet(filter):
    dp.pya.alert('O arquivo xlsx será manipulado. Clique em Ok.')
    box = dp.tk.Tk()
    box.title('Carregando')
    dp.center_window(box)
    progress = dp.ttk.Progressbar(box, orient='horizontal', length=250, mode='determinate')
    progress.pack(pady=20)
    
    # dp.center_window(box)
    
    def start_process():
        progress.start()
        try:
            FILE_PATH = get_downloaded_file(DOWNLOAD_DIR)
            handle_worksheet(FILE_PATH, filter)
        except Exception as error:
            dp.pya.alert(f'Erro ao tentar manipular o arquivo: {error}')
            print(error)
        finally:
            progress.stop()
            box.destroy()
        
    thread = dp.th.Thread(target=start_process)
    thread.start()
    box.mainloop()
    
    dp.pya.alert('Arquivo tratado. Encerrar aplicação.')


# EXECUTA TUDO E +
def run_application(user, password, filter):
    try:
        driver = create_driver()
        handle_website_1(driver, user, password, filter)
        wait_handle_worksheet(filter)
        driver.quit()
    except Exception as error:
        dp.pya.alert(f'Erro ao executar a aplicação: {error}')
        print(error)


