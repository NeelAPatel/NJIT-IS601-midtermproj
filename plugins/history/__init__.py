from decimal import Decimal
import sys
from commands import Command 
import data_store
import os
import pandas as pd
import logging as log

class HistoryCommand(Command): 
    def execute(self, *args):         

        if len(args) == 0: 
            self.default_response()
        else: 
            # Check which subcommand and fetch that method to trigger
            switchcase_dict = {
                'show': self.show, 
                'clear': self.clear, 
                'last': self.last,
                'dummy' : self.dummy,
                'add' : self.add,
                'save': self.save,
                'delrow': self.delrow,
                'reloadfile': self.reloadfile 
            }
            method = switchcase_dict.get(args[0], self.default_response)
            method(*args)
    
    def default_response(self, *args):
        print()
        print('The history plugin used for interacting with the calculations stored in memory.')
        print('')
        print('Usage: ')
        print('  history <command> [parameters]')
        print('')
        print('Commands: ')
        print('  show            prints out the dataframe table')
        print('  dummy           appends a dummy calculation of "5*4 = 20"')
        print('  last            shows last calculation stored in the table')
        print('  delrow [num]    delete specified row from history')
        print('  save            firm saves the table to the csv file location')
        print('  reloadfile      reloads file from known history path')
        print('  clear           empties the dataframe table')
        print('     usage:  history delete 1')
        print('')
        
    
    def show(self, *args): 
        # shows dataframe output
        try:
            print(data_store.hist_df)
        except Exception as e:
            print(f"Error showing history: {e}")

    def dummy(self, *args): 

        new_row = {'operand': '*', 'num1': 5, 'num2': 4, 'result': 20}
        data_store.hist_df.loc[len(data_store.hist_df)] = new_row

        print("New Dummy calculation added: ")
        print(new_row)
        # print()
        # print("Result table: ")
        # print(data_store.hist_df)

        #Autosave
        self.save()
        print()


    def last(self, *args): 
        try:
            print(data_store.hist_df.iloc[-1])
        except IndexError:
            print("Data frame is empty.")
    

    def add(self, *args): 
        log.debug(args)
        
        # used by calc to save new data with args[0] = null
        try: 
            new_row = {'operand': args[2], 'num1': args[1] , 'num2': args[3], 'result': args[4]}
            data_store.hist_df.loc[len(data_store.hist_df)] = new_row
            print("New calculation added: ")
            # print(new_row)
            # print("Result table: ")
            # print(data_store.hist_df)
            
            #Autosave
            self.save()
            print()
        except IndexError: 
            log.error("Error: Incorrect arguments for 'history add': $> history add <num1> <sign> <num2> <result>")
        
    def delrow (self, *args): 
        log.debug(args)

        if len(args) != 2:
            print("Error: Incorrect number of arguments provided.")
            return
        try:
            row_index = int(args[1])
            data_store.hist_df = data_store.hist_df.drop(data_store.hist_df.index[row_index])
            data_store.hist_df.reset_index(drop=True, inplace=True)  # Resetting the index and dropping the old index column
            log.info("Row deleted")
            self.save()
        except ValueError:
            log.error("Error: Provided index is not an integer.")
        except KeyError:
            log.error(f"Error: No row found at index {row_index}.")
        except IndexError: 
            log.error(f"Error: Table is empty, no rows to delete.")


    # works
    def save(self, *args):
        my_df = data_store.hist_df
        my_df.to_csv(data_store.hist_path, index=False)
        print("!! Saved to File !!")
        log.info("File saved")

    def reloadfile(self, *args):
            try:
                data_store.hist_df = pd.read_csv(data_store.hist_path)
                log.info("File read successfully")
                # Resetting the index in case there are gaps from previous operations
                data_store.hist_df.reset_index(drop=True, inplace=True)
                print("Data successfully reloaded from file.")
                log.info("File reloaded")

                self.show()
            except FileNotFoundError:
                log.error(f"File not found at {data_store.hist_path}. Ensure the file path is correct.")
            except pd.errors.EmptyDataError:
                log.error("File is empty. Starting with an empty DataFrame.")
                data_store.hist_df = pd.DataFrame()  # Creating an empty DataFrame
            except Exception as e:
                log.error(f"An error occurred while reloading from file: {e}")

    def clear(self, *args):
        #empties dataframe and saves
        try:
            data_store.hist_df = data_store.hist_df[0:0]  # Clearing the DataFrame
            log.info("History - Dataframe cleared")
            print("Cleared history dataframe!")
            
            #Autosave
            self.save()
        except Exception as e:
            log.error(f"History - Error clearing history: {e}")