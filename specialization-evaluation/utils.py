specializations = [
    'backend_engineer',
    'frontend_engineer',
    'full_stack_engineer',
    'mobile_engineer',
    'blockchain_engineer',
    'platform_engineer',
    'data_engineer',
    'ml_engineer',
    'data_scientist',
    'quant_engineer',
    'devops_engineer',
    'sre_engineer',
    'cloud_engineer',
    'build_release_engineer',
    'systems_engineer',
    'automation_engineer',
    'security_engineer',
    'ui_ux_engineer',
    'software_architect',
    'embedded_engineer',
    'firmware_engineer',
    'desktop_engineer',
    'bios_engineer',
    'ar_vr_engineer',
    'iot_engineer',
    'quantum_engineer',
    'graphics_engineer',
    'image_processing_engineer',
    'video_processing_engineer',
    'game_engineer',
    'unity_engineer',
    'unreal_engineer',
    'sales_engineer',
    'nocode_engineer',
    'sap_engineer',
    'salesforce_engineer',
    'servicenow_engineer',
    'workday_engineer',
    'engineering_manager',
    'qa_engineer',
    'data_analyst',
    'sys_admin',
    'dba',
]


def merge_reviewed_data(df, target_column):
    for index in df.index:
        reviewer1_data = set(df.at[index, f'{target_column}_reviewer1'].split(', '))
        reviewer2_data = set(df.at[index, f'{target_column}_reviewer2'].split(', '))

        reviewed_data = set.intersection(reviewer1_data, reviewer2_data)
        reviewed_data.discard('')
        ambiguous_reviewed_data = set.symmetric_difference(reviewer1_data, reviewer2_data)
        ambiguous_reviewed_data.discard('')

        df.at[index, target_column] = str(reviewed_data)
        df.at[index, f'ambiguous_{target_column}'] = str(ambiguous_reviewed_data)
        df.replace('set()', '', inplace=True)


def convert_to_snake_case(specialization):
    replacements = {
        'developer': 'engineer',
        'unreal engine': 'unreal',
        'system administrator': 'sys_admin',
        'database administrator': 'dba',
        '-': '_',
        ' & ': '_',
        '/': '_',
        ' ': '_',
    }

    for key, value in replacements.items():
        specialization = specialization.lower().replace(key, value)

    return specialization
