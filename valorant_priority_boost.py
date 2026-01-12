import time
import random
import ctypes
import sys
import os

try:
    import psutil
    import win32api
    import win32process
    import win32gui
except ImportError:
    print("Installation des dépendances requises...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil", "pywin32"])
    import psutil
    import win32api
    import win32process
    import win32gui

# Constantes de priorité Windows
ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000  # 32768

# Couleurs console
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_console()
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 50)
    print("       VALORANT PRIORITY BOOSTER")
    print("=" * 50)
    print(f"{Colors.RESET}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_valorant_process():
    """Trouve le processus Valorant"""
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            if proc.info['name'] == 'VALORANT-Win64-Shipping.exe':
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def set_priority(pid, priority_class=ABOVE_NORMAL_PRIORITY_CLASS):
    """Applique la priorité au processus"""
    try:
        handle = win32api.OpenProcess(0x1F0FFF, False, pid)  # PROCESS_ALL_ACCESS
        win32process.SetPriorityClass(handle, priority_class)
        win32api.CloseHandle(handle)
        return True
    except Exception as e:
        print(f"{Colors.RED}[ERREUR] Impossible de modifier la priorité: {e}{Colors.RESET}")
        return False

def get_foreground_process_name():
    """Retourne le nom du processus de la fenêtre active"""
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except:
        return None

def random_delay():
    """Génère un délai aléatoire entre 8 et 14 secondes"""
    return random.randint(8, 14)

def main():
    # Vérifie les droits admin
    if not is_admin():
        print(f"{Colors.RED}[!] Ce script doit être lancé en tant qu'administrateur !{Colors.RESET}")
        print(f"{Colors.YELLOW}    Clic droit -> Exécuter en tant qu'administrateur{Colors.RESET}")
        input("\nAppuyez sur Entrée pour quitter...")
        sys.exit(1)
    
    print_banner()
    print(f"{Colors.GREEN}[OK] Droits administrateur confirmés{Colors.RESET}")
    print(f"\n{Colors.YELLOW}En attente de Valorant...{Colors.RESET}\n")
    
    valorant_running = False
    valorant_focused = False
    initial_done = False
    
    while True:
        pid = get_valorant_process()
        
        if pid:
            # Valorant vient de se lancer
            if not valorant_running:
                print(f"{Colors.GREEN}[OK] Valorant détecté ! (PID: {pid}){Colors.RESET}")
                valorant_running = True
                initial_done = False
            
            # Séquence initiale (2 applications avec délais aléatoires)
            if not initial_done:
                # Premier passage
                delay1 = random_delay()
                print(f"{Colors.CYAN}[1/2] Attente de {delay1} secondes...{Colors.RESET}")
                time.sleep(delay1)
                
                if set_priority(pid):
                    print(f"{Colors.GREEN}[1/2] Priorité 'Supérieure à la normale' appliquée !{Colors.RESET}")
                
                # Deuxième passage
                delay2 = random_delay()
                print(f"{Colors.CYAN}[2/2] Attente de {delay2} secondes...{Colors.RESET}")
                time.sleep(delay2)
                
                if set_priority(pid):
                    print(f"{Colors.GREEN}[2/2] Priorité réappliquée !{Colors.RESET}")
                
                print(f"\n{Colors.GREEN}{'=' * 50}")
                print("   Séquence initiale terminée !")
                print(f"{'=' * 50}{Colors.RESET}")
                print(f"\n{Colors.YELLOW}Surveillance des retours Windows active...{Colors.RESET}\n")
                
                initial_done = True
                valorant_focused = True
            
            # Détection du focus de la fenêtre
            current_focus = get_foreground_process_name()
            
            if current_focus == 'VALORANT-Win64-Shipping.exe':
                if not valorant_focused:
                    print(f"{Colors.CYAN}[RETOUR] Valorant de nouveau au premier plan{Colors.RESET}")
                    delay3 = random_delay()
                    print(f"{Colors.CYAN}[BOOST] Attente de {delay3} secondes...{Colors.RESET}")
                    time.sleep(delay3)
                    
                    if set_priority(pid):
                        print(f"{Colors.GREEN}[BOOST] Priorité réappliquée !{Colors.RESET}\n")
                    
                    valorant_focused = True
            else:
                if valorant_focused and initial_done:
                    print(f"{Colors.YELLOW}[INFO] Retour Windows détecté...{Colors.RESET}")
                    valorant_focused = False
        
        else:
            # Valorant fermé
            if valorant_running:
                print(f"{Colors.YELLOW}[INFO] Valorant fermé. En attente de relance...{Colors.RESET}\n")
                valorant_running = False
                valorant_focused = False
                initial_done = False
        
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INFO] Script arrêté par l'utilisateur.{Colors.RESET}")
        sys.exit(0)
