def get_header_indices(header_line):
    header_indices = []
    first_line_deliminated = header_line.split(',')
    first_line_stripped = []
    for column in first_line_deliminated:
        cell = column.strip()
        first_line_stripped.append(cell)
    try:
        start_index = first_line_stripped.index('Start')
    except:
        start_index = 0
    try:
        end_index = first_line_stripped.index('End')
    except:
        end_index = 1
    try:
        rt_index = first_line_stripped.index('RT')
    except:
        rt_index = 2
    try:
        name_index = first_line_stripped.index('Name')
    except:
        name_index = 3
    try:
        mw_index = first_line_stripped.index('MW')
#         mw_index = first_line_stripped.index('Quasi Mol ion')
        
    except:
        mw_index = 4
    try:
        ncarbons_index = first_line_stripped.index('#Carbons')
    except:
        ncarbons_index = 5
    try:
        quasi_mol_ion_index = first_line_stripped.index('Quasi Mol ion')
    except:
        ncarbons_index = 6   
    header_indices = [start_index, end_index, rt_index, name_index, mw_index, ncarbons_index, quasi_mol_ion_index]
    return header_indices

def make_profile_list(profile_file_lines):
    profile_list = []
    header_line = profile_file_lines[0]
    header_indices = get_header_indices(header_line)

    start_index = header_indices[0]
    end_index = header_indices[1]
    rt_index = header_indices[2]
    name_index = header_indices[3]
    mw_index = header_indices[4]
    ncarbons_index = header_indices[5]
    quasi_mol_ion_index = header_indices[6]
    
    list_ncarbons = []
    list_names = []
    list_ncarbons.append(1)
    
    profile_count = 0
    exception_count = 0
    for line in profile_file_lines[1:]:
        current_line = line.split(',')
        start,end,rt = [0,0,0]
        name = 'unknown'
        ncarbons = 0
        mw, quasi_mol_ion = [0.0,0.0]
        try:
            start = float(current_line[start_index])
            end = float(current_line[end_index])
            rt = float(current_line[rt_index])
            try:
                name = str(current_line[name_index])
                duplicate_counter = 0
                while name in list_names:
                    duplicate_counter += 1
                    name = str(name + str(duplicate_counter))
                
                if len(name) < 1:
                    name = str("unknown at " + str(rt))
                    while name in list_names:
                        duplicate_counter += 1
                        name = str(name + str(duplicate_counter))
            except:
                name = str("unknown at " + str(rt))
                while name in list_names:
                    duplicate_counter += 1
                    name = str(name + str(duplicate_counter))
            try:
                mw = float(current_line[mw_index])
                if mw < 1:
                    mw = 1
            except:
                mw = 1
            try:
                ncarbons = int(current_line[ncarbons_index])
                if ncarbons < 1:
                    ncarbons = math.floor(sum(list_ncarbons)/len(list_ncarbons))

            except:
                ncarbons = math.floor(sum(list_ncarbons)/len(list_ncarbons))
            
            try:
                quasi_mol_ion = float(current_line[quasi_mol_ion_index])
                if quasi_mol_ion < 1:
                    quasi_mol_ion = 1
            except:
                quasi_mol_ion = 1
                
            list_ncarbons.append(ncarbons)
            list_names.append(name)
                
            mwfloor = math.floor(mw)
            decimal = mw - mwfloor
            if decimal >= 0.7:
                mw = mwfloor + 1
            else:
                mw = mwfloor
            compound = [name, start, rt, end, mw, ncarbons, quasi_mol_ion]
#             print(compound)
            profile_list.append(compound)
            profile_count += 1
        except:
            print("Exception in generating profile_list")
            exception_count += 1
#             return profile_list
        
    return profile_list, profile_count, exception_count