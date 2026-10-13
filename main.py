import sys
import requests
import json
import os
from settings import token
from time import sleep
from tqdm import tqdm

class YandexDisk:
    url_dog = "https://dog.ceo/api/breed/"
    urlYD = "https://cloud-api.yandex.net"

    def __init__(self):
        self.token = token
        self.headers = {"Authorization": f"OAuth {self.token}"}
        self.pbar = None

    def enter_dog_breed(self):
        while True:
            folder_name = input("\nEnter a dog breed (0 for exit), but keep in mind that the" +
                                "\n" + "entire file path must be strictly under 250 characters: ")
            if folder_name == "0":
                self.pbar = tqdm(total=100, desc="Closing Program", file=sys.stdout)
                self.pbar.update(100)
                self.pbar.set_postfix_str("Program closed!")
                self.pbar.close()
                print("Application closed successfully!")
                sys.exit(0)
            self.pbar = tqdm(total=100, desc=f"Program progress for breed '{folder_name}'", file=sys.stdout,
                             bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]")
            sleep(1)
            self.pbar.update(10)
            self.pbar.set_postfix_str(f"Breed '{folder_name}' entered successfully!")
            response = requests.get(self.url_dog + f"{folder_name}/list")
            if response.status_code == 200:
                self.pbar.write(f"Request for a '{folder_name}' information was successful!")
                sleep(1)
                self.pbar.update(10)
                self.pbar.set_postfix_str(f"Information for a '{folder_name}' was received successfully!")
            else:
                self.pbar.write(f"Request for a {folder_name} information was not successful: {response.status_code}")
                self.pbar.write(response.json()["message"])
                self.pbar.close()
                sys.exit(0)
            if len(response.json()["message"]) == 0:
                self.get_dog_url(folder_name, 80)
            else:
                sub_breeds = response.json()["message"]
                total_sub_breeds = len(sub_breeds)
                partial = 80 / total_sub_breeds
                for index, sub_breed in enumerate(sub_breeds):
                    folder = folder_name + "/" + sub_breed
                    if index == total_sub_breeds - 1:
                        remaining_share = 100 - self.pbar.n
                        self.get_dog_url(folder, remaining_share)
                    else:
                        self.get_dog_url(folder, partial)
            self.pbar.set_postfix_str(f"Program for a breed '{folder_name}' finished successfully!")
            self.pbar.close()
            sys.stdout.write("Application processed breed successfully!\n")
            sys.stdout.flush()

    def get_dog_url(self, folder_name, partial):
        target_n = self.pbar.n + partial
        response = requests.get(self.url_dog + f"{folder_name}/images/random")
        if response.status_code == 200:
            self.pbar.write(f"Request for a {folder_name} url was successful!")
        else:
            self.pbar.write(f"Request for a {folder_name} url was not successful: {response.status_code}")
            self.pbar.write(response.json()["message"])
            self.pbar.close()
            sys.exit(0)
        sleep(1)
        self.pbar.update(partial / 4)
        self.pbar.set_postfix_str(f"Request for a {folder_name} url was successful!")
        url = response.json()["message"]
        name = response.json()["message"].split("/")[-1].split(".")[0]
        response2 = requests.get(url)
        if response2.status_code == 200:
            self.pbar.write(f"Request for a {folder_name} image was successful!")
        else:
            self.pbar.write(f"Request for a {folder_name} image was not successful: {response2.status_code}")
            self.pbar.write(response2.json()["message"])
            self.pbar.close()
            sys.exit(0)
        sleep(1)
        self.pbar.update(partial / 4)
        self.pbar.set_postfix_str(f"Request for a {folder_name} image was successful!")
        if "/" in folder_name:
            file_name = folder_name.replace("/", "-")
        else:
            file_name = folder_name
        file_extension = response2.headers["content-type"].split('/')[1]
        image_size = response2.headers["content-length"]
        if "/" in folder_name:
            folder_name = folder_name.split("/")[0]
        self.create_folder(folder_name, partial / 4)
        name_file = file_name + "-" + name
        content = response2.content
        last_share = target_n - self.pbar.n
        self.upload_file_to_folder(folder_name, name_file, file_extension, content, last_share)
        self.get_dog_file_info(name_file, file_extension, image_size)

    def create_folder(self, folder_name, partial_share):
        response = requests.put(self.urlYD + "/v1/disk/resources/" + f"?path=%2F{folder_name}", headers=self.headers)
        if response.status_code == 201:
            self.pbar.write(f"Folder {folder_name} was created successfully!")
            sleep(1)
            self.pbar.update(partial_share)
            self.pbar.set_postfix_str(f"Folder {folder_name} was created successfully!")
        elif response.status_code == 409:
            self.pbar.write(f"Folder {folder_name} already exists!")
            sleep(1)
            self.pbar.update(partial_share)
            self.pbar.set_postfix_str(f"Folder {folder_name} already exists!")
        else:
            self.pbar.write(f"Folder {folder_name} was not created: {response.status_code}")
            self.pbar.write(response.json()["message"])
            self.pbar.close()
            sys.exit(0)

    def upload_file_to_folder(self, folder_name, name_file, file_extension, content, partial_share):
            response = requests.get(
                self.urlYD + "/v1/disk/resources/upload" + f"?path=%2F{folder_name}%2F{name_file}.{file_extension}" + "&overwrite=true",
                headers=self.headers)
            if response.status_code == 200:
                self.pbar.write(f"Link to upload file {name_file}.{file_extension} received successfully!")
            elif response.status_code == 409:
                self.pbar.write(f"File {name_file}.{file_extension} already exists!")
            else:
                self.pbar.write(f"Error: {response.status_code}")
                self.pbar.write(response.json()["message"])
                self.pbar.close()
                sys.exit(0)
            path = response.json()["href"]
            response2 = requests.put(path, content)
            if response2.status_code == 201:
                self.pbar.write(f"File {name_file}.{file_extension} uploaded successfully!")
                sleep(1)
                self.pbar.update(partial_share)
                self.pbar.set_postfix_str(f"File {name_file}.{file_extension} uploaded successfully!")
            else:
                self.pbar.write(f"Loading error: {response2.status_code}")
                self.pbar.write(response2.json()["message"])
                self.pbar.close()
                sys.exit(0)

    @staticmethod
    def get_dog_file_info(file_name, file_extension, image_size):
        data = {
            f"{file_name}.{file_extension}": image_size
        }
        file_exists = os.path.exists("image_size_data.json")
        if not file_exists:
            image_size_data = {}
            initial_data = {
                "Dog picture file name": "Size in bytes"
            }
            image_size_data.update(initial_data)
            image_size_data.update(data)
            with open("image_size_data.json", "w", encoding="utf-8") as file:
                json.dump(image_size_data, file, ensure_ascii=False, indent=4)
        else:
            with open("image_size_data.json", "r", encoding="utf-8") as file:
                image_size_data = json.load(file)
                image_size_data.update(data)
            with open("image_size_data.json", "w", encoding="utf-8") as file:
                json.dump(image_size_data, file, ensure_ascii=False, indent=4)

YD = YandexDisk()

YD.enter_dog_breed()
