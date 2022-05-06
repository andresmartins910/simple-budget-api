import pandas as pd

def json_to_excel(data):

    new_data = {}

    data_dict = list(data)[-1]

    if data_dict == 'expenses':
            value = pd.DataFrame(data[data_dict])
            new_data['expenses'] = value
    else:
        for dict in data[data_dict]:
            value = pd.DataFrame(dict['expenses'])
            new_data[f'budget{dict["budget_id"]}'] = value


    writer = pd.ExcelWriter('app/reports_temp/report.xlsx')

    for sheet_name in new_data.keys():
        new_data[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)

        index = 0
        for column in new_data[sheet_name]:
            column_width = max(new_data[sheet_name][column].astype(str).map(len).max(), len(column))
            writer.sheets[sheet_name].set_column(index, index, column_width)
            index += 1

    writer.save()

    return ''
