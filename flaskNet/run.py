from flaskNet import start
from colorama import Fore,init
init()

v = '1.1'

if __name__ == '__main__':
    try:
        print(Fore.LIGHTBLUE_EX+f'FlaskNet {v}v'+Fore.RESET)
        print(Fore.LIGHTBLUE_EX+'Developed by Md.Eiadur Rahman'+Fore.RESET)
        start()
    except Exception as err:
        print(Fore.RED+'something went wrong......'+Fore.RESET)
        print(Fore.LIGHTYELLOW_EX+f'ERROR :\n{err}'+Fore.RESET)
