import pandas as pd
folder_file_txt_destination = input() 
read_file = pd.read_csv(r'{}'.format(folder_file_txt_destination))
file_destination_csv = input()
read_file.to_csv(r'{}'.format(file_destination_csv),index= None)
