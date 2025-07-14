from streamlit.testing.v1 import AppTest

# Inicializa o app
at = AppTest.from_file("app/streamlit_ui.py")

# Executa a primeira renderização
at.run()

# Acessa o valor atual do menu lateral (deve ser 'Upload' por padrão)
print(at.sidebar.radio[0].value)  # Deve imprimir 'Upload'

# Agora simula mudar para "Normalize"
at.sidebar.radio[0].set_value("Normalize")
at.run()

# Verifica se a nova tela foi renderizada
print(at.title[0].value)  # Deve ser "Fix & Normalize Data" ou equivalente

