# Requires colorama; install with: pip install colorama

from colorama import Fore, Style, init

# Initialize colorama for Windows terminals
init(autoreset=True)

print(Fore.GREEN + "Success! Colorama is working.")
print(Fore.CYAN + "This text is cyan.")
print(Fore.RED + "This text is red.")
print(Style.BRIGHT + "And this text is bright/bold.")
