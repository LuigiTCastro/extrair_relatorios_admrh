import Dependencies as dp

def execution():
    try:
        try:
            dp.show_box()
        except Exception as error:
            print(error)
            try:
                driver = dp.create_driver
                error_msg = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.XPATH, "//div[@class='error-page-container']")))
                if error_msg:
                    initial_page = dp.WebDriverWait(driver, 10).until(dp.EC.element_to_be_clickable((dp.By.ID, 'form:btn_voltar_inicio')))
                    initial_page.click()
                    dp.show_box()
                else:
                    dp.pya.alert('Tratamento da exceção não funcionou.')
                    dp.pya.alert('Encerrar aplicação.')
                    driver.quit()
            except Exception as error:
                print(f'Erro ao tentar executar aplicação: {error}.')
                dp.pya.alert(f'Erro ao tentar executar aplicação.')
        return
    except Exception as error:
        print(f'Erro ao tentar executar aplicação: {error}.')
        dp.pya.alert(f'Erro ao tentar executar aplicação.')
        

execution()