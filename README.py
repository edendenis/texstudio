#!/usr/bin/env python
# coding: utf-8

# # Como instalar/configurar/usar o ``TeXstudio`` no `Linux Ubuntu`
# 
# ## Resumo
# 
# Neste documento estão contidos os principais comandos e configurações para configurar/instalar/usar o `TeXstudio` no `Linux Ubuntu`.
# 
# ## _Abstract_
# 
# _This document contains the main commands and settings for configuring/installing/use `TeXstudio` on `Linux Ubuntu`._ 

# ### Construído com
# 
# Esta seção deve listar todas as principais estruturas/bibliotecas usadas para inicializar seu projeto, bem como a sequência de instalação. Deixe quaisquer complementos/plugins para a seção de agradecimentos. Aqui estão alguns exemplos.
# 
# * [![Texlive](https://img.shields.io/badge/Texlive-3776AB?style=flat-square&logo=latex&logoColor=white)](https://tug.org/texlive/)
# * [![JabRef](https://img.shields.io/badge/JabRef-44A833?style=flat-square&logo=latex&logoColor=white)](https://www.jabref.org/)
# * [![Texstudio](https://img.shields.io/badge/Texstudio-008080?style=flat-square&logo=latex&logoColor=white)](https://www.texstudio.org/)
# * [![MathPix](https://img.shields.io/badge/MathPix-008080?style=flat-square&logo=MathPix&logoColor=white)](https://mathpix.com/)
# 
# <p align="right">(<a href="#readme-top">voltar ao topo</a>)</p>
# 

# ## Descrição [2]
# 
# ### ``TeXstudio``
# 
# O `TeXstudio` é um ambiente integrado de desenvolvimento (IDE) gratuito e de código aberto projetado especificamente para facilitar a criação e edição de documentos LaTeX, um sistema de composição tipográfica amplamente utilizado para produzir documentos científicos, acadêmicos e técnicos de alta qualidade. Com recursos como realce de sintaxe, correção automática, assistência de código e visualização em tempo real, o `TeXstudio` torna o processo de escrita e formatação de documentos LaTeX mais eficiente e acessível. Ele oferece uma interface amigável para a configuração de projetos, gerenciamento de bibliotecas de referências, bem como integração com o TeX Live e outras distribuições LaTeX, tornando-o uma escolha popular entre autores e pesquisadores que buscam uma ferramenta poderosa e conveniente para produzir documentos técnico-científicos de alta qualidade.

# ## 1. Configurar/Instalar o `TeXstudio` no Linux Ubuntu [1]
# 
# Para configurar/instalar o `TeXstudio` no Ubuntu, você pode seguir os seguintes passos:
# 
# 1. Abra o `Terminal Emulator`. Você pode fazer isso pressionando: `Ctrl + Alt + T`
# 

# 2. Certifique-se de que seu sistema esteja limpo e atualizado.
# 
#     2.1 Limpar o `cache` do gerenciador de pacotes `apt`. Especificamente, ele remove todos os arquivos de pacotes (`.deb`) baixados pelo `apt` e armazenados em `/var/cache/apt/archives/`. Digite o seguinte comando: `sudo apt clean` 
#     
#     2.2 Remover pacotes `.deb` antigos ou duplicados do cache local. É útil para liberar espaço, pois remove apenas os pacotes que não podem mais ser baixados (ou seja, versões antigas de pacotes que foram atualizados). Digite o seguinte comando: `sudo apt autoclean`
# 
#     2.3 Remover pacotes que foram automaticamente instalados para satisfazer as dependências de outros pacotes e que não são mais necessários. Digite o seguinte comando: `sudo apt autoremove -y`
# 
#     2.4 Buscar as atualizações disponíveis para os pacotes que estão instalados em seu sistema. Digite o seguinte comando e pressione `Enter`: `sudo apt update`
# 
#     2.5 **Corrigir pacotes quebrados**: Isso atualizará a lista de pacotes disponíveis e tentará corrigir pacotes quebrados ou com dependências ausentes: `sudo apt --fix-broken install`
# 
#     2.6 Limpar o `cache` do gerenciador de pacotes `apt`. Especificamente, ele remove todos os arquivos de pacotes (`.deb`) baixados pelo `apt` e armazenados em `/var/cache/apt/archives/`. Digite o seguinte comando: `sudo apt clean` 
#     
#     2.7 Para ver a lista de pacotes a serem atualizados, digite o seguinte comando e pressione `Enter`:  `sudo apt list --upgradable`
# 
#     2.8 Realmente atualizar os pacotes instalados para as suas versões mais recentes, com base na última vez que você executou `sudo apt update`. Digite o seguinte comando e pressione `Enter`: `sudo apt full-upgrade -y`
#     

# 3. **Instale o `TeXstudio`:** Você pode instalar o `TeXstudio` diretamente a partir dos repositórios oficiais do Ubuntu usando o comando apt. Execute o seguinte comando para instalar: `sudo apt install texstudio -y`
# 
#     - O sistema pode pedir a sua senha de administrador para confirmar a instalação. Digite a senha e pressione `Enter`.
# 
#     - Execute o comando a seguir para corrigir a interrupção no `dpkg`: `sudo dpkg --configure -a`
# 
# - **Confirme a instalação:** Caso peça a senha, depois de digitar sua senha, o sistema perguntará se você deseja continuar com a instalação. Digite `Y` e pressione `Enter` para confirmar.
# 
#     - O `TeXstudio` será baixado e instalado automaticamente no seu sistema.
# 
# 5. Verifique a instalação: Após a instalação ser concluída com sucesso, você pode verificar se o `TeXstudio` está instalado corretamente, executando o comando: texstudio --version`
# 
#     - Isso exibirá a versão do `TeXstudio` instalada no seu sistema.
# 
# Agora, você deve ter o `TeXstudio` instalado no seu Ubuntu e pronto para ser usado para edição de documentos LaTeX. Você pode iniciar o `TeXstudio` a partir do menu de aplicativos ou usando o comando `TeXstudio` no terminal.
# 

# ## 1.1 Código completo para configurar/instalar/usar
# 
# Para configurar/instalar/usar o `TeXstudio` no `Linux Ubuntu` sem precisar digitar linha por linha, você pode seguir estas etapas:
# 
# 1. Abra o `Terminal Emulator`. Você pode fazer isso pressionando: `Ctrl + Alt + T`
# 
# 2. Digite o seguinte comando e pressione `Enter`:
# 
#     ```
#     sudo apt clean                                                            
#     sudo apt autoclean
#     sudo apt autoremove -y
#     sudo apt update
#     sudo apt --fix-broken install
#     sudo apt clean
#     sudo apt list --upgradable
#     sudo apt full-upgrade -y
#     sudo apt install texstudio -y
#     texstudio
#     texstudio --version
#     ```

# ## 2. Habilitar o `Auto Save All Files` no `TeXstudio`
# 
# Para habilitar o `Auto Save All Files` no ``TeXstudio``, siga os passos abaixo:
# 
# 1. Abra o ``TeXstudio``.
# 
# 2. Vá para o menu `Options` (`Opções`) no topo da janela.
# 
# 3. Selecione `Configure TeXstudio...` (`Configurar TeXstudio...`).
# 
# 4. Clique na janela de configurações, clique em `Show Advanced Options` (`Mostrar Opções Avançadas`) na canto inferior esquerdo.
# 
# 5. Clique na janela de configurações, clique em `Adv. Editor` (`Editor Avançado`) na barra lateral esquerda.
# 
# 6. Se precisar, role a barra de rolagem veritical para baixo, no painel à direita, você verá a opção `Auto Save All Files` (Auto Salvar Todos os Arquivos).
# 
# 7. Marque a caixa ao lado de `Auto Save All Files` para habilitar essa funcionalidade.
# 
#     6.1 Você pode ajustar o intervalo de tempo para o `Auto Save All Files` de acordo com suas preferências. É recomendado colocar entre cerva de `5 minutes` a `10 minutes`, no máximo `20 minutes`, para que não fique salvando a todo momento e, ao mesmo tempo, caso o trabalho seja perdido por falta de energia elétrica, por exemplo, não será perdido todo ou muito do trabalho desenvolvido.
# 
# Isso deve ativar o `AutoSave` no `TeXstudio`, garantindo que suas alterações sejam salvas automaticamente em intervalos regulares. Lembre-se de clicar em "OK" para confirmar as alterações e fechar a janela de configurações.
# 

# ## 3. Habilitar o `Auto-recompile` no `TeXstudio`
# 
# 1. Abra o ``TeXstudio``.
# 
# 2. Vá para o menu `Options` (`Opções`) no topo da janela.
# 
# 3. Selecione `Configure TeXstudio...` (`Configurar TeXstudio...`).
# 
# 4. Clique na janela de configurações, clique em `Internal PDF Viewer` (`Visualizador PDF Interno`) na barra lateral esquerda.
# 
# 5. Se precisar, role a barra de rolagem veritical para baixo, no painel à direita, você verá a opção `Auto-recompile documents on changes` (`Auto-recompilar`). Marque a caixa ao lado de `Auto-recompile documents on changes` para habilitar essa funcionalidade.
# 
# Isso deve ativar o `Auto-recompile documents on changes` no `TeXstudio`, garantindo que suas alterações sejam compiladas automaticamente após as alterações. Lembre-se de clicar em `"OK"` para confirmar as alterações e fechar a janela de configurações.
# 

# ## 4. Habilitar o `Show Whitespace` no `TeXstudio`
# 
# 1. Abra o ``TeXstudio``.
# 
# 2. Vá para o menu `Options` (`Opções`) no topo da janela.
# 
# 3. Selecione `Configure TeXstudio...` (`Configurar TeXstudio...`).
# 
# 4. Clique na janela de configurações, clique em `Adv. Editor` (`Editor Avançcado`) na barra lateral esquerda.
# 
# 5. Se precisar, role a barra de rolagem veritical para baixo, no painel à direita, você verá a opção `Show Whitespace` (`Mostrar Espaço em Branco`). Marque a caixa ao lado de `Auto-recompile documents on changes` para habilitar essa funcionalidade.
# 
# Isso deve ativar o `Auto-recompile documents on changes` no `TeXstudio`, garantindo que suas alterações sejam compiladas automaticamente após as alterações. Lembre-se de clicar em `"OK"` para confirmar as alterações e fechar a janela de configurações.
# 

# ## Referências
# 
# [1] OPENAI. ***Instalar o texstudio no linux ubuntu:*** Disponível em: <https://chat.openai.com/c/f308ebb4-ad7e-4ff2-a634-90ffd0c558f8> (texto adaptado). ChatGPT. Acessado em: 29/09/2023 18:56.
# 
# [2] OPENAI. ***Vs code: editor popular:*** Disponível em: <https://chat.openai.com/c/b640a25d-f8e3-4922-8a3b-ed74a2657e42> (texto adaptado). ChatGPT. Acessado em: 14/11/2023 18:56.
# 
# [3] OPENAI. ***Ativar autosave no `texstudio`.*** Disponível em: <https://chat.openai.com/c/210ca6d2-7da5-4830-890a-b8e1cb0ee7ee> (texto adaptado). ChatGPT. Acessado em: 27/11/2023 10:44.
# 
# [4] OPENAI. ***Texstudio auto-compilation/live preview feature (latex tips)/solution-51.*** Disponível em: <https://www.youtube.com/watch?v=hO1LmNtKg1w> (texto adaptado). ChatGPT. Acessado em: 18/01/2024 08:46.
# 
