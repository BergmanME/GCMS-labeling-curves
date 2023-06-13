def get_areas_df(file_path_input):
    print("fetching areas")
    areas_df = get_csv(return_type='df', title='Areas', initialdir=file_path_input, skip_blank_lines=True, skiprows=1)
    areas_df.columns.values[0] = 'SampleID'
    areas_df.head()
    return areas_df
def get_sampleID_from_area(sample_file):
    ## works to return sample ID from full info line
    ## #"+CI Scan (rt: 4.762 min) 210505_NH3-pos-split-scan_361-R2.D  Subtract "
    start_character = "\\"
    end_character = ".D"
    start_index = sample_file.rfind(start_character) + len(start_character)
    end_index = sample_file.rfind(end_character)
    sampleID = sample_file[start_index:end_index]
    return sampleID
def get_area_tables(profile_df, areas_df):
    print("Separating features by sample")
    areas_df_split = [y for x, y in areas_df.groupby('SampleID', as_index=False)] # Split dataframe by SampleID

    profile_headers = profile_df.columns.tolist()
    extra_headers = ['sampleID', 'in_profile', 'flag','RT_difference']
    area_headers = areas_df.columns.tolist()
    feature_headers = extra_headers + area_headers
    columnheaders = profile_headers + extra_headers + area_headers
    all_rows = [columnheaders]

    simplified_headers = profile_headers
    all_simplified_features = []

    first_run_for_sample = True
    for index1,profilefeature in profile_df.iterrows():
        profileID, profileRT, lowerrt, upperrt = profilefeature['Peak'], profilefeature['RT'], profilefeature['Start'], profilefeature['End']
#         print(f"Working on: {profileID}")
        profile_line = profilefeature.tolist()
        this_simplified_feature = profilefeature.tolist()
        this_feature = []
        flag, previous_sample, first_run_for_feature = None, None, True
        sample_counter = 0 
        for sample_df in areas_df_split:
            sample_df['RT'] = pd.to_numeric(sample_df['RT'], errors='coerce') # Sets non numeric as NaN
            sample_df = sample_df[sample_df['RT'] > 0]
            if len(sample_df) > 0: # Only process data files and lines with at least 1 features
                sample_file = sample_df['SampleID'].iloc[0]
                sampleID = get_sampleID_from_area(sample_file)                 
#                 print(f"processing: {sampleID}")
                if first_run_for_sample:
                    simplified_headers.append(sampleID)
                in_profile=False
                possible_features = []

    #                 rt_index = sample_df.columns.get_loc("RT")
    #                 area_index = sample_df.columns.get_loc("Area")
                for index1,feature in sample_df.iterrows():
                    this_feature = []
                    rt,area = feature['RT'],feature['Area']
                    if lowerrt < rt < upperrt: # feature rt is within profile rt bounds
                        # feature confirmed in profile
                        flag = None
                        in_profile = True
                        RT_difference = rt - profileRT
                        RT_difference = round(RT_difference,4)
                        this_feature=[sampleID, in_profile, flag, RT_difference]
                        feature_values = feature.values.tolist()
                        this_feature = this_feature + feature_values
                        possible_features.append(this_feature)

                if in_profile:
                    sample_counter += 1
                    possible_features_df = pd.DataFrame(possible_features,columns=feature_headers)
                    this_feature_df = possible_features_df[possible_features_df['RT_difference'] == possible_features_df['RT_difference'].min()]
                    this_feature_df = this_feature_df.loc[0]
                    area = this_feature_df['Area']
                    this_feature = this_feature_df.tolist()
                    this_row = profile_line + this_feature
                    all_rows.append(this_row)
                    this_simplified_feature.append(area)
    #                 print(f"{profileID} added for {sampleID}")
                else:
                    this_simplified_feature.append(None)
    #                 print(f"{profileID} not found for {sampleID}")
        all_simplified_features.append(this_simplified_feature)
        first_run_for_sample = False
        print(f"{profileID} found in {sample_counter} samples.")
            
    #         print(f"{profileID} completed")
#     simplified_area_table = simplified_headers + all_simplified_features
    detailed_areas_df = pd.DataFrame(all_rows,columns=columnheaders)
    simplified_areas_df = pd.DataFrame(all_simplified_features,columns=simplified_headers)
    return(detailed_areas_df, simplified_areas_df)

def ask_areas():
    '''ask if user wants to get area data'''
    from tkinter.messagebox import askyesno
    title = 'Process peak area data?'
    message = 'Would you like to process peak area data?'
    get_areas = askyesno(title=title, message=message)
    return get_areas

def process_areas(file_path_input, file_path_output):
    get_areas = ask_areas()
    if get_areas is True:
        areas_df = get_areas_df(file_path_input)
        print("Processing areas data table...")
        detailed_areas_df, simplified_areas_df = get_area_tables(profile_df, areas_df)
        print("Dataframe for all features with details complete")
        output_file_name1 = 'detailed_areas_df.csv'
        output_file_name2 = 'simplified_areas_df.csv'
        print(f"Exporting {output_file_name1} and {output_file_name2} to {file_path_output}")
        output_file_name_path1 = os.path.join(file_path_output, output_file_name1)
        output_file_name_path2 = os.path.join(file_path_output, output_file_name2)
        try:
            detailed_rawF_df.to_csv(output_file_name_path1, sep=',', na_rep='', index=False)
            print("Export complete")
        except:
            print(f"Error in exporting {output_file_name1} to {output_file_name_path1}.\nMake sure a file with this name is not already open.\nContinuing without exporting this file.")
        try:
            simplified_rawF_df.to_csv(output_file_name_path2, sep=',', na_rep='', index=False, header=False)
            print("Export complete")
        except:
            print(f"Error in exporting {output_file_name2} to {output_file_name_path2}.\nMake sure a file with this name is not already open.\nContinuing without exporting this file.")

        simplified_areas_df.head()
    else:
        quit()
        
process_areas(file_path_input, file_path_output)
    

