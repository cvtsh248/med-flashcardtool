import random
import pandas as pd
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class mainApplication():
    def __init__(self, flashcard_directory):
        self.flashcard_directory = flashcard_directory
        self.cards_df = None

    def loadCardsIntoDataframe(self, topics=[]):
        csv_files = []
        for root, _, files in os.walk(self.flashcard_directory):
            for file in files:
                if file.endswith(".csv"):
                    csv_files.append(os.path.join(root, file))

        if len(topics) == 0:
            dataframes = []
            for file in csv_files:
                df = pd.read_csv(file)
                dataframes.append(df)
            dataframe = pd.concat(dataframes, axis=0, ignore_index=True)
            self.cards_df = dataframe
            return dataframe
        elif len(topics) > 0:
            filtered_dataframes = []
            for file in csv_files:
                if (lambda s, lst: all(sub in s for sub in lst))(file, topics):
                    df = pd.read_csv(file)
                    filtered_dataframes.append(df)
            if len(filtered_dataframes) > 0:
                dataframe = pd.concat(filtered_dataframes, axis=0, ignore_index=True)
                self.cards_df = dataframe
                return dataframe
            else:
                raise Exception
        else:
            raise Exception
        
    def sortLoadedCards(self, tags=[]):
        if len(tags) == 0:
            return
        elif len(tags) > 0:
            filtered_dataframe = pd.DataFrame(columns=["side_a","side_b","tags"])
            for index, row in self.cards_df.iterrows():
                card_tag = row["tags"].split(";")
                if any(x in tags for x in card_tag):
                    filtered_dataframe = pd.concat([filtered_dataframe, row.to_frame().T], ignore_index=True)
            self.cards_df = filtered_dataframe
            return filtered_dataframe
        
    def displayCard(self, index, side='side_a'):
        return str(self.cards_df.loc[index][side]).replace("\\n", "\n")
    
    def gameMaster(self):
        print(bcolors.HEADER+"Flashcard revision"+bcolors.ENDC)

        csv_files = []
        for root, _, files in os.walk(self.flashcard_directory):
            for file in files:
                if file.endswith(".csv"):
                    csv_files.append(os.path.join(root, file))

        module = []
        tbls = []
        for file in csv_files:
            file = file.split('/')
            module.append(file[1])
            tbls.append([file[1],file[2]])
        module = list(set(module)) 

        for mod in module:
            print(bcolors.BOLD+mod+bcolors.ENDC)
            
        mods_ = input("Enter modules, deliminated by commas (no input means everything): ")
        if mods_ != "":
            mods_ = mods_.split(", ")

            for tbl in tbls:
                if tbl[0] in mods_:
                    print(bcolors.BOLD+tbl[1]+bcolors.ENDC)

            tbls_ = input("Enter TBLs, deliminated by commas (no input means everything): ")
            tbls_ = tbls_.split(", ")

            self.loadCardsIntoDataframe(topics=mods_+tbls_)
        else:
            self.loadCardsIntoDataframe()
        
        tags = input("Enter any tags, deliminated by commas (no input means no filtering): ")
        tags.split(", ")
        self.sortLoadedCards(tags=tags)

        print("-----------------------------------------------")

        print(bcolors.OKGREEN+"Revision Starting"+bcolors.ENDC)

        selected_indices = []
        while True:
            selected_index = 0

            if len(selected_indices) == len(self.cards_df.index):
                print(bcolors.BOLD+"-----------------------------------------------"+bcolors.ENDC)
                yn = input(bcolors.WARNING+"You have revised all the cards. Would you like to go again (y/n)?\n"+bcolors.ENDC)
                if "y" in yn or "Y" in yn:
                    selected_indices = []
                else:
                    break

            while selected_index in selected_indices:
                selected_index = random.randint(0,len(self.cards_df.index)-1)

            selected_indices.append(selected_index)
            print("-----------------------------------------------")
            print(bcolors.BOLD+self.displayCard(selected_index)+bcolors.ENDC)
            input("")
            print(bcolors.OKCYAN+self.displayCard(selected_index, side="side_b")+bcolors.ENDC)
            input("")
            print("-----------------------------------------------")

m = mainApplication('flashcards')
m.gameMaster()