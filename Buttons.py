import Dependencies as dp


def center_window(window):
    """Centraliza uma janela na tela."""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_reqwidth()
    window_height = window.winfo_reqheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f'+{x}+{y}')
    
    
def on_button_click1(box, user, password):
    box.destroy()
    filter = 'ATIVOS'
    dp.run_application(user, password, filter)

    
def on_button_click2(box, user, password):
    box.destroy()
    filter = 'GERAL'
    dp.run_application(user, password, filter)


def show_second_box(user, password):
    box = dp.tk.Tk()
    box.title('Dialog box')
    box.geometry('300x200')
    center_window(box)
    
    label = dp.tk.Label(box, text="Selecione uma opção:")
    label.pack(pady=15)
    
    button1 = dp.tk.Button(box, text='Relatório de Ativos', command=dp.partial(on_button_click1, box, user, password), width=25, height=1)
    button1.pack(pady=10)
    
    button2 = dp.tk.Button(box, text='Relatório Geral', command=dp.partial(on_button_click2, box, user, password), width=25, height=1)
    button2.pack(pady=10)
    
    box.mainloop()


def get_entry_text(entry_user, entry_password, box):
    entry_user = entry_user.get()
    entry_password = entry_password.get()
    box.destroy()
    return entry_user, entry_password 


# PEGAR DADOS DE LOGIN
# def get_credentials(entry_user, entry_password, box):
#     credentials = get_entry_text(entry_user, entry_password, box)
#     user = None
#     password = None
#     with open(credentials, 'r', encoding='utf-8') as txt:
#         for line in txt:
#             if line.startswith('Usuário:'):
#                 user = line.split(':')[1].strip()
#             elif line.startswith('Senha:'):
#                 password = line.split(':')[1].strip()
#             if user is not None and password is not None:
#                 break

#     return user, password


def show_box():
    box = dp.tk.Tk()
    box.title('Dialog box')
    box.geometry('300x200')
    center_window(box)
    
    dp.tk.Label(box).pack(expand=True, pady=4)

    label = dp.tk.Label(box, text='Usuário:')
    label.pack(expand=True, pady=4)
    entry_user = dp.tk.Entry(box, width=40)
    entry_user.pack(pady=4)

    label = dp.tk.Label(box, text='Senha:')
    label.pack(expand=True, pady=4)
    entry_password = dp.tk.Entry(box, width=40, show='*')
    entry_password.pack(pady=4)
    
    # label = dp.tk.Label(box, text='Inserir caminho do arquivo txt com credenciais:')
    # label.pack(expand=True, pady=4)
    
    # file_path = '.\login\caminho.txt'
    # default_file_path = ''
        
    # if dp.os.path.exists(file_path):
    #     with open(file_path, 'r', encoding='utf-8') as txt:
    #         for line in txt:
    #             default_file_path = line.strip()
    #             if default_file_path:
    #                 break
    
    # entry.insert(0, default_file_path)
    
    
    submit_button = dp.tk.Button(box, text='Enviar', command=lambda: on_submit(entry_user, entry_password, box))
    submit_button.pack(pady=10)
    
    dp.tk.Label(box).pack(expand=True, pady=4)
    
    box.mainloop()


def on_submit(entry_user, entry_password, box):
    user, password = get_entry_text(entry_user, entry_password, box)
    if user is not None and password is not None:
        show_second_box(user, password)
    else:
        print("Usuário ou senha não encontrados.")

