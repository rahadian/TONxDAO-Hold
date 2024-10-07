import sys,os,time
from core.headers import headers
from core.token import get_token
from core.info import get_info, get_fullname, get_username, banner, get_daily_info, get_daily_claim, get_tiktok_info, get_tiktok_claim
from core.task import Task
from threading import Thread
from datetime import datetime

class Game:
    def __init__(self):
        self.data_file = self.file_path(file_name="data.txt")
        
    def file_path(self, file_name: str):
        # Get the directory of the file that called this method
        caller_dir = os.path.dirname(
            os.path.abspath(sys._getframe(1).f_code.co_filename)
        )

        # Join the caller directory with the file name to form the full file path
        file_path = os.path.join(caller_dir, file_name)

        return file_path

    def clear_terminal(self):
        """Clears the terminal screen."""
        if os.name == 'nt':
            os.system('cls')  # For Windows
        else:
            os.system('clear')  # For Linux/Unix
    
    def check_and_mine(self,token,fullname):
        task = Task([token])
        mining_result = task.start_mining()
        if not mining_result:
            print(f"Mining stopped for: {fullname} due to low energy.")
            return False
        return True
                    
    def main(self):
        while True:
            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            data = open(self.data_file, "r").read().splitlines()
            tokens = []
            
            for data_entry in data:
                token = get_token(data=data_entry)
                if token:
                    tokens.append(token)
                    info = get_info(token=token)
                    fullname = get_fullname(token=token)
                    username = get_username(token=token)
                    daily_info = get_daily_info(token=token)
                    daily_claim = get_daily_claim(token=token)
                    tiktok_info = get_tiktok_info(token=token)
                    tiktok_claim = get_tiktok_claim(token=token)
                    print("===============================")
                    if daily_info == "True":
                        print(f"Daily claim available: {daily_info}")
                        print(f"Daily claim : {daily_claim}")
                    else:
                        print(f"Daily claim available: {daily_info}")
                    print(f"{dt_string}")
                    print(f"Processing account: {fullname}")
                    
                    if(tiktok_claim == "Task already claimed"):
                        print(f"tiktok task claim : {tiktok_claim}")
                    else:
                        print(f"processing task tiktok ...")
                        tiktok_info
                        tiktok_claim
                    
                    if self.check_and_mine(token, fullname):
                        return True
                    else:
                        print(f"Mining stopped due to low energy, moving to next user.")
                        print("===============================")
                    
            print(f"{dt_string}")  
            print("All users have low energy, pausing for 4 hours...")
            time.sleep(14400)
            self.clear_terminal()
                        
                    

if __name__ == "__main__":
    banner()
    try:
        game = Game()
        game.main()
    except KeyboardInterrupt:
        sys.exit()