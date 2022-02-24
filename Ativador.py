import time
import paramiko
from keyboard import on_press  # Bloco de imports de packages
from os import execl

# Variaveis Globais
global olt
global nolt

# Variaveis de Login OLT
username = 'USER'  # Digite o usuario de login do SSH
password = 'SENHA'  # Digite a senha de login do SSH
port = 22  # Altere a porta de login do SSH caso seja diferente


def onkeypress(event):
    if event.name == 'right ctrl':
        execl('Ativacao.exe', __file__)   # Essa função faz o reboot do script com o botão ctrl direito do teclado
        exit()


def ativacao():
    olts()
    print(f"\nA olt {nolt} foi selecionada! \n")
    slot = input("Informe o SLOT de conexão! \n")
    pon = input("Informe o PON de conexão! \n")
    ont = input("Informe a ONT de conexão! \n")  # Esse bloco é referente as informações que precisam ser digitadas
    desc1 = input("Informe a DESCRIÇÃO 1! \n")
    desc2 = input("Informe a DESCRIÇÃO 2! \n")
    mac = input("Informe o MAC! \n")
    vlan = input("Digite a VLAN!")
    print('Enviando os comandos AGUARDE!')

    at1 = f'ENT-ONT::ONT-1-1-{slot}-{pon}-{ont}::::DESC1="{desc1}",DESC2="{desc2}",SERNUM={mac},SWVERPLND=DISABLED;'
    at2 = f'ED-ONT::ONT-1-1-{slot}-{pon}-{ont}:::::IS;'
    at3 = f'ENT-ONTCARD::ONTCARD-1-1-{slot}-{pon}-{ont}-1:::10_100BASET,1,0::IS;'
    at4 = f'ENT-LOGPORT::ONTL2UNI-1-1-{slot}-{pon}-{ont}-1-1:::;'  # Esse bloco é referente aos comandos que
    at5 = f'ED-ONTVEIP::ONTVEIP-1-1-{slot}-{pon}-{ont}-1-1:::::IS;'  # serão enviados via ssh para a olt
    at6 = f'SET-QOS-USQUEUE::ONTL2UNIQ-1-1-{slot}-{pon}-{ont}-1-1-0::::USBWPROFNAME=HSI_1G_UP;'
    at7 = f'SET-VLANPORT::ONTL2UNI-1-1-{slot}-{pon}-{ont}-1-1:::MAXNUCMACADR=32,CMITMAXNUMMACADDR=1;'
    at8 = f'ENT-VLANEGPORT::ONTL2UNI-1-1-{slot}-{pon}-{ont}-1-1:::0,{vlan}:PORTTRANSMODE=UNTAGGED;'
    at9 = f'SET-VLANPORT::ONTL2UNI-1-1-{slot}-{pon}-{ont}-1-1:::DEFAULTCVLAN={vlan};'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=olt, username=username, password=password, port=port)  # Login SSH na OLT e abertura do painel
    commands = ssh.invoke_shell()
    time.sleep(5)

    commands.send(f"{at1} {at2} {at3} {at4} {at5} {at6} {at7} {at8} {at9}")
    print('\n\n\n\n\n\n\n\n\nAlteração realizada com sucesso!')  # Envio dos comandos para a OLT
    ativacao()


def olts():
    global olt
    global nolt
    print('\nSelecione uma OLT!\n')
    oltinput = input('1 - OLT 1 \n'
                     '2 - OLT 2\n'
                     '3 - OLT 3 \n'
                     '4 - OLT 4 \n')
    if oltinput == '1':
        olt = 'IP OLT'
        nolt = 'OLT 1'
    elif oltinput == '2':  # Essa função é referente a seleção da OLT.
        olt = 'IP OLT'
        nolt = 'OLT 2'
    elif oltinput == '3':
        olt = 'IP OLT'
        nolt = 'OLT 3'
    elif oltinput == '4':
        olt = 'IP OLT'
        nolt = 'OLT 4'
    else:
        print('\nOpção Invalida! \n')
        olts()


print('Digite o número correspondente a opção desejada e aperte ENTER! \n\n\n\n')

on_press(onkeypress)  # Chama a função de reboot caso o CTRL DIREITO seja pressionado
ativacao()
