### Application uploads dog images of a breed (and all sub-breeds, if any) indicated by you from https://dog.ceo/dog-api/  to your Yandex Disk folder (https://360.yandex.ru/disk/), and also creates and modifies a JSON file with names and sizes of the uploaded dog images.

#### Application needs an OAuth token from https://yandex.ru/dev/disk/poligon/

#### This token should be placed in the variable "token" in module "settings.py" (as shown by the module "settings.example.py").

#### A folder for these dog images on your Yandex Disk is created by the application. The folder name is a dog breed name indicated by you.

#### The command "YD = YandexDisk()" creates an object "YD" of the "YandexDisk" class, which allows you to use its methods.

#### The method "YD.enter_dog_breed()" runs a loop that asks you to enter a text (dog’s breed) or a number 0 (to exit the loop), requests an information about the dog’s breed in https://dog.ceo/dog-api and calls the method "get_dog_url(self, folder_name, partial)".

#### The method "get_dog_url(self, folder_name, partial)" loads dog image(s) from https://dog.ceo/dog-api and calls following methods:

#### 1) method "create_folder(self, folder_name, partial_share)" creates a folder with a dog’s breed name in your Yandex Disk.

#### 2) method "upload_file_to_folder(folder_name, name_file, file_extension, content, last_share)" loads file(s) with dog images to the aforementioned folder in your Yandex Disk.

#### 3) static method "get_dog_file_info(file_name, file_extension, image_size)" is responsible for creating and modifying a JSON file with names and sizes of the files uploaded to the aforementioned folder in your Yandex Disk. The parameters of this static method are all the "String" type. The name of JSON file is "image_size_data.json"

#### Application informs you about successful (or not) execution of all important steps, and also illustrates the application progress by a graphic-and-numeric scale from 0 to 100%.
