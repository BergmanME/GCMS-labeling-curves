## Functions for loading input files

## ask for file
import os
import tkinter as tk
import pandas as pd


def ask_csv_file(titleprompt, file_path):
    csvfile = open(tk.filedialog.askopenfilename(title=titleprompt,
                                                 initialdir=file_path,
                                                 filetypes=(("CSV files", ".csv"), ("all files", "*.*"))))
    return csvfile

## Get csv file
def get_csv_file(csvfilename, file_path):
    csv_path = os.path.join(file_path, csvfilename)
    csvfile = open(csv_path)
    return csvfile

## get file lines for csv file
def get_file_lines(csvfile):
    input_file_lines = csvfile.readlines()
    return input_file_lines

#Export csv file

def export_csv(export_data, output_notice, output_name, file_path_output, open_output):
    import csv
    import os.path
    csvfile = tk.filedialog.asksaveasfilename(initialdir=file_path_output, initialfile=output_name,
                                           defaultextension=".csv",
                                           filetypes=(("CSV files", ".csv"), ("all files", "*.*")),
                                           title="Output File Name")
    print('Writing ', output_notice, ' into .csv file')
    with open(csvfile, "w") as output:
        write_csv = csv.writer(output, lineterminator='\n')
        write_csv.writerows(export_data)
    print(output_notice, ' file will now open')
    if open_output == True:
        os.startfile(csvfile)
    return csvfile

#export_csv(super_simple_labelling_data_for_csv, "Super simple fractional labelling output", "Simple_Fractional_Label.csv")

def make_list_into_df(list):
    df = pd.DataFrame(list)
    new_headers = df.iloc[0]
    df = df[1:]
    df.columns = new_headers
    return df

def remove_rt_data_from_df(df):
    bad_index = df.index[df.iloc[:,0] == '\n']
    bad_index = bad_index[0] - 1
    new_df = df.iloc[0:bad_index,:]
    return new_df

def concat_raw_labelling_data(list_of_dfs):
    new_list_of_dfs = []
    for dataframe in list_of_dfs:
        this_df = remove_rt_data_from_df(dataframe)
        new_list_of_dfs.append(this_df)
    all_samples_F_df = pd.concat(new_list_of_dfs)
    return all_samples_F_df

def stripformat(df):
    df.columns = [col.strip() for col in df.columns]
    Samplecol = df.iloc[:,0]
    new_df = df.replace('[\'Peak not found\']', 0, regex=True)
    new_df['sample (fractional labelling)'] = Samplecol
    return new_df

## output_aligned_peak_table()
def output_aligned_peak_table(areas_for_csv, file_path_output, open_output):
    csv_file = export_csv(areas_for_csv, "aligned peak area table", "Output_areas.csv", file_path_output, open_output)
    print("Done function: output_aligned_peak_table()")
    return csv_file

print('defined function for exporting aligned peak table as csv')