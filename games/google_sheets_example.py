import pygsheets
import pandas as pd


class GSheetsLogger:
    def __init__(self, service_key=r"C:\Users\17743\OneDrive\Documents\keys\hult-auto-reservation-1a0360021964.json"):
        # authorization
        self.gc = pygsheets.authorize(service_file=service_key)
        self.sh = None
        self.wks = None

    def open_spreadsheet(self, name='Reservations Log'):
        # open google spreadsheet (where 'Reservations Log' is the name of my sheet)
        self.sh = self.gc.open(name)

    def select_sheet(self, sheet_idx=0):
        # select work sheet at sheet_idx inside of google spread sheet
        self.wks = self.sh[sheet_idx]

    def update_log(self, df, overwrite=False):
        # you can also get the values of sheet as dataframe
        df_rb = self.wks.get_as_df()
        num_rows = df_rb.shape[0]

        if num_rows and not overwrite:
            # append df to existing data in data sheet, +2 to account starting location due to index 0 and header
            self.wks.set_dataframe(df, (num_rows+2, 1), copy_head=False, extend=True, fit=False)
        else:
            # write from beginning location, include header
            self.wks.set_dataframe(df, (1, 1))

    def get_log(self):
        return self.wks.get_as_df()



if __name__ == '__main__':
    # Create empty dataframe
    df = pd.DataFrame()

    # Create a column
    df['date'] = ['02/20/2024']
    df['day'] = ['Tuesday']
    df['time'] = ['06:00 PM']
    df['status'] = ['Booked']
    df['name'] = ['Dario Martinovic']
    df['email'] = ['dario.vivamus@gmail.com']
    df['phone'] = ['7743187224']

    logger = GSheetsLogger()
    logger.open_spreadsheet('Test Sheet')
    logger.select_sheet(0)
    logger.update_log(df)


