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
            # method/function dictionary
            switchcase_dict = {
                'show': self.show, 
                'clear': self.clear, 
                'last': self.last,
                'dummy' : self.dummy,
                'add' : self.add,
                'save': self.save,
                'delete': self.delete,
                'reloadfile': self.reloadfile 
            }
            #get method from args and store that method in variable 'method'
            method = switchcase_dict.get(args[0], self.default_response)

            #execute that method
            method(*args)

    
    def default_response(self, *args):
        message = ('Usage: \n'
            '  history <command> [parameters]\n'
            '     The history plugin used for interacting with the calculations stored in memory.\n'
            '\n'
            'Commands: \n'
            '  show            prints out the dataframe table\n'
            '  dummy           appends a dummy calculation of "5*4 = 20"\n'
            '  last            shows last calculation stored in the table\n'
            '  delete [num]    delete specified row from history\n'
            '  save            firm saves the table to the csv file location\n'
            '  reloadfile      reloads file from known history path\n'
            '  clear           empties the dataframe table\n'
            '     usage:  history delete 1\n'
        )
        print(message)
        
    
    def show(self, *args): 
        # shows dataframe output
        try:
            print(data_store.hist_df)
        except Exception as e:
            log.error(f"Error showing history: {e}")

    def dummy(self, *args): 
        # insert dummy row
        new_row = {'num1': 5, 'operand': '*',  'num2': 4, 'result': 20}
        data_store.hist_df.loc[len(data_store.hist_df)] = new_row

        print("New Dummy calculation added: ")
        print(new_row)

        #autosave
        self.save(*args)


    def last(self, *args):
        #retrieves last added calculation 
        try:
            print(data_store.hist_df.iloc[-1])
        except IndexError:
            log.error("Data frame is empty.")
    

    def add(self, *args): 
        # used by calc to save new data with args[0] = null
        log.debug(args)
        try: 
            if (len(args) != 5): 
                raise IndexError
            elif (args[2] not in ['+', '-', '*', '/']):
                raise ValueError
            
            new_row = {'num1': args[1] , 'operand': args[2],  'num2': args[3], 'result': args[4]}
            data_store.hist_df.loc[len(data_store.hist_df)] = new_row
            print("New calculation added: ")
            print(new_row)

            #autosave
            self.save(*args)
        except IndexError: 
            log.error("Error: Incorrect arguments for 'history add': $> history add <num1> <sign> <num2> <result>")
        except ValueError: 
            log.error("Error: Invalid sign symbol for 'history add': sign= +, -, *, / ")
            return
        
    def delete (self, *args): 
        #Deletes a specific row in the dataframe --> Resets indexes
        log.debug(args)

        # If arguments dont match, then error
        if len(args) != 2:
            log.error("Error: Incorrect number of arguments for 'delete'. Usage history delete [row_num]")
            return
        
        # If dataframe is empty, cannot delete anything
        if data_store.hist_df.empty:
            log.error("Error: Table is empty, no rows to delete.")
            return
        
        try:
            # Get row index from parameter
            row_index = int(args[1])

            # Delete specific row and reset/drop old index column
            data_store.hist_df.drop(index=row_index, inplace=True)
            data_store.hist_df.reset_index(drop=True, inplace=True)
            print(f"Row {row_index} deleted successfully.")

            #autosave
            self.save()
        except ValueError:
            log.error("Error: Provided index is not an integer.")
            return
        except KeyError:
            log.error(f"Error: No row found at index {row_index}.")
            return

    def save(self, *args):
        #Saves file to local 
        my_df = data_store.hist_df
        my_df.to_csv(data_store.hist_path, index=False)
        print("!! Saved to File !!\n")
        log.info("File saved")

    def reloadfile(self, *args):
        # Reloads the CSV file from local into memory
        try:
            #Read file from memory
            data_store.hist_df = pd.read_csv(data_store.hist_path)
            log.info("File read successfully")

            # Resetting the index in case there are gaps from previous operations
            data_store.hist_df.reset_index(drop=True, inplace=True)
            
            # Now its successful
            print("Data successfully reloaded from file.")
            log.info("File reloaded")

            self.show()
        except FileNotFoundError:
            log.error(f"File not found at {data_store.hist_path}. Ensure the file path is correct.")
        except pd.errors.EmptyDataError:
            log.error("File is empty. Starting with an empty DataFrame.")
            #resetting dataframe to ensure columns exist at all times
            columns = ['num1', 'operand', 'num2', 'result']
            data_store.hist_df = pd.DataFrame(columns=columns)  # Creating an empty DataFrame
            log.info("New History dataframe created")

            #autosave
            self.save(*args)
        except Exception as e:
            log.error(f"An error occurred while reloading from file: {e}")

    def clear(self, *args):
        #empties dataframe and saves
        try:
            data_store.hist_df = data_store.hist_df[0:0]  # Clearing the DataFrame
            log.info("History - Dataframe cleared")
            print("Cleared history dataframe!")

            #autosave
            self.save(*args)
        except Exception as e:
            log.error(f"History - Error clearing history: {e}")