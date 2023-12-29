import pandas as pd
from ast import literal_eval
from utils import specializations, merge_reviewed_data, convert_to_snake_case


task = 'Muti-class specialization evaluation'
target_column = 'reviewed_specialization'

evaluate_file = './data/' + task + '.csv'
df = pd.read_csv(evaluate_file, converters={'current_specialization': literal_eval}).fillna('')

if target_column not in df.columns:
    merge_reviewed_data(df, target_column)

counter = pd.DataFrame(
    index = specializations,
    columns = ['relevant_instances', 'retrieved_instances', 'relevant_retrieved_instances', 'other_correct_predictions'],
).fillna(0)


for index in df.index:
    reviewed_data = df.at[index, target_column]
    sampled_data = [convert_to_snake_case(d['name']) for d in df.at[index, 'current_specialization']]
    is_match = 0
    not_match = 0
    if f'ambiguous_{target_column}' in df.columns:
        ambiguous_reviewed_data = df.at[index, f'ambiguous_{target_column}']
    else:
        ambiguous_reviewed_data = ''

    for specialization in specializations:
        if specialization not in ambiguous_reviewed_data:
            if (specialization in reviewed_data) and (specialization in sampled_data):
                counter.loc[specialization, ['relevant_instances', 'retrieved_instances', 'relevant_retrieved_instances']] += 1
                is_match = 1
            elif specialization in reviewed_data:
                counter.at[specialization, 'relevant_instances'] += 1
                not_match = 1
            elif specialization in sampled_data:
                counter.at[specialization, 'retrieved_instances'] += 1 
            else:
                counter.at[specialization, 'other_correct_predictions'] += 1

    if is_match == 1 and not_match == 1:
        df.at[index, f'{target_column}_result'] = 'partially correct'
    elif is_match == 0 and not_match == 1:
        df.at[index, f'{target_column}_result'] = 'wrong'
    else:
        df.at[index, f'{target_column}_result'] = None


print(counter.head())

counter.to_csv('counter.csv')
df.to_csv('results.csv', index=False)
