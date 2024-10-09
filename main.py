import sys, os, time
from core.headers import headers
from core.token import get_token
from core.info import (get_info, get_fullname, get_username, banner, 
                       get_daily_info, get_daily_claim, get_tiktok_info, 
                       get_tiktok_claim, get_emoji_info, get_emoji_claim)
from core.task import Task
from threading import Thread
from datetime import datetime
import concurrent.futures

class Game:
    def __init__(self):
        self.data_file = self.file_path(file_name="data.txt")
        
    def file_path(self, file_name: str):
        caller_dir = os.path.dirname(os.path.abspath(sys._getframe(1).f_code.co_filename))
        file_path = os.path.join(caller_dir, file_name)
        return file_path

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def process_user(self, data_entry):
        token = get_token(data=data_entry)
        if not token:
            return

        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        
        info = get_info(token=token)
        fullname = get_fullname(token=token)
        username = get_username(token=token)
        daily_info = get_daily_info(token=token)
        daily_claim = get_daily_claim(token=token)
        tiktok_info = get_tiktok_info(token=token)
        tiktok_claim = get_tiktok_claim(token=token)
        emoji_info = get_emoji_info(token=token)
        emoji_claim = get_emoji_claim(token=token)
        
        print("===============================")
        print(f"{dt_string}")
        print(f"Processing account: {fullname}")
        
        if daily_info == "True":
            print(f"Daily claim available: {daily_info}")
            print(f"Daily claim : {daily_claim}")
        else:
            print(f"Daily claim available: {daily_info}")
        
        if tiktok_claim == "Task already claimed":
            print(f"tiktok task claim : {tiktok_claim}")
        else:
            print(f"processing task tiktok ...")
            tiktok_info
            tiktok_claim
            print(f"processing task tiktok: Done")
        
        if emoji_claim == "Task already claimed":
            print(f"emoji task claim : {emoji_claim}")
        else:
            print(f"processing task emoji ...")
            emoji_info
            emoji_claim
            print(f"processing task emoji: Done")
        print("===============================")
        
        task = Task([token])
        mining_result = task.start_mining()
        if not mining_result:
            print(f"Mining stopped for: {fullname} due to low energy.")
            return False
        return True

    def main(self):
        while True:
            with open(self.data_file, "r") as file:
                data = file.read().splitlines()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.process_user, data_entry) for data_entry in data]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
                if not any(results):
                    now = datetime.now()
                    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                    print(f"{dt_string}")  
                    print("All users have low energy, pausing for 4 hours...")
                    time.sleep(14400)
                    self.clear_terminal()
            
            if not any(results):
                now = datetime.now()
                dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
                print(f"{dt_string}")  
                print("All users have low energy, pausing for 4 hours...")
                time.sleep(14400)
                self.clear_terminal()
            else:
                break

if __name__ == "__main__":
    banner()
    try:
        game = Game()
        game.main()
    except KeyboardInterrupt:
        sys.exit()