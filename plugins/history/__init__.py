from decimal import Decimal
import sys
from commands import Command 
import data_store
import os


class HistoryCommand(Command): 
    def execute(self, *args):         

        if len(args) == 0: 
            self.default_response()
        else: 
            switchcase_dict = {
                'show': self.show, 
                'clear': self.clear, 
                'last': self.last,
                'add' : self.add,
                'save': self.save,
                'delete': self.delete,
                'erase': self.erase 
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
        print('  add             adds a static calculation of "5*4 = 20"')
        print('  save            firm saves the table to the csv file location')
        print('  delete [num]    delete specified row from history')
        print('     usage:  history delete 1')
        print('')
        
    
    def show(self, *args): 
        hist_df = data_store.hist_df
        print(hist_df)
        print()
        # complete

    def clear(self, *args):
        hist_df = data_store.hist_df
        hist_df = hist_df.iloc[0:0]
        print("History Cleared!")
        print()
        #complete

    def last(self, *args): 
        hist_df = data_store.hist_df
        #check if table is empty 
        # if empty, fail gracefully
        latest_row = hist_df.iloc[-1]
        print(latest_row)
    

    def add(self, *args): 
        hist_df = data_store.hist_df
        new_row = {'operand': '*', 'num1': 5, 'num2': 4, 'result': 20}
        hist_df.loc[len(hist_df)] = new_row
        print("added: ")
        print(new_row)
        print(hist_df)

        print()

    def save(self, *args):
        hist_df = data_store.hist_df
        hist_df.to_csv(data_store.hist_path, index=False)
        print("Save csv")


    def delete (self, *args): 
        print("deleting row" + args[1])
        hist_df = data_store.hist_df
        hist_id = hist_df.drop(args[1])

    def erase(self, *args): 
        os.remove(data_store.hist_path)
        print("erased file")
        sys.exit(0)
        
