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

        # return method()
    def default_response(self, *args):
        print()
        print('The history plugin used for interacting with the calculations stored in memory.')
        print('')
        print('Usage: ')
        print('  history <command> [parameters]')
        print('')
        print('Commands: ')
        print('  show            prints out the dataframe table')
        print('  clear           empties the dataframe table')
        print('  last            shows last calculation stored in the table')
        print('  dummy           appends a dummy calculation of "5*4 = 20"')
        print('  delrow [num]    delete specified row from history')
        print('  save            firm saves the table to the csv file location')
        print('  reloadfile      reloads file from known history path')
        print('     usage:  history delete 1')
        print('')
        
    
    def show(self, *args): 
        try:
            print(data_store.hist_df)
        except Exception as e:
            print(f"Error showing history: {e}")
        # complete

    def clear(self, *args):
        try:
            log.info("History - Clearing dataframe to empty table")
            data_store.hist_df = data_store.hist_df[0:0]  # Clearing the DataFrame
            log.info("History - Dataframe cleared")
            print("Cleared history dataframe!")
            
            
            self.save()  # Save after clearing
        except Exception as e:
            log.error(f"History - Error clearing history: {e}")
        #complete

    def last(self, *args): 
        try:
            print(data_store.hist_df.iloc[-1])
        except IndexError:
            print("Data frame is empty.")
    

    def add(self, *args): 
        # used by calc to save new data with args[0] = null
        print("hist ", args)        
        
        

        new_row = {'operand': args[2], 'num1': args[1] , 'num2': args[3], 'result': args[4]}
        log.info("")
        # new_row = {'operand': '*', 'num1': 5, 'num2': 4, 'result': 20}
        data_store.hist_df.loc[len(data_store.hist_df)] = new_row

        print("added: ")
        print(new_row)
        print("Result table: ")
        print(data_store.hist_df)
        self.save()
        print()

    def dummy(self, *args): 
        log.info("")
        new_row = {'operand': '*', 'num1': 5, 'num2': 4, 'result': 20}
        data_store.hist_df.loc[len(data_store.hist_df)] = new_row

        print("added: ")
        print(new_row)
        print("Result table: ")
        print(data_store.hist_df)
        self.save()
        print()

    # works
    def save(self, *args):
        my_df = data_store.hist_df
        my_df.to_csv(data_store.hist_path, index=False)
        print("!! Saved to File !!")


    def delrow (self, *args): 

        if len(args) != 2:
            print("Error: Incorrect number of arguments provided.")
            return
        try:
            row_index = int(args[1])
            data_store.hist_df = data_store.hist_df.drop(data_store.hist_df.index[row_index])
            data_store.hist_df.reset_index(drop=True, inplace=True)  # Resetting the index and dropping the old index column
            self.save()
        except ValueError:
            log.error("Error: Provided index is not an integer.")
        
        except KeyError:
            log.error(f"Error: No row found at index {row_index}.")
        except IndexError: 
            log.error(f"Error: Table is empty, no rows to delete.")


    def reloadfile(self, *args):
            try:
                data_store.hist_df = pd.read_csv(data_store.hist_path)
                # Resetting the index in case there are gaps from previous operations
                data_store.hist_df.reset_index(drop=True, inplace=True)
                print("Data successfully reloaded from file.")
            except FileNotFoundError:
                log.error(f"File not found at {data_store.hist_path}. Ensure the file path is correct.")
            except pd.errors.EmptyDataError:
                log.error("File is empty. Starting with an empty DataFrame.")
                data_store.hist_df = pd.DataFrame()  # Creating an empty DataFrame
            except Exception as e:
                log.error(f"An error occurred while reloading from file: {e}")