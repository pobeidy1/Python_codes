import os

def create_folder_structure(proj_name, data='data', output='output', figures='figures',
                            src='src', scripts='scripts', docs='docs'):
    if not os.path.exists(proj_name):
        os.makedirs(proj_name)
    folders = [os.path.join(proj_name, folder) for folder in [data, output, figures, src, docs]]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    def create_src_subfolders(proj_name):
        src_path = os.path.join(proj_name, 'src')
        if not os.path.exists(src_path):
            os.makedirs(src_path)

        functions_path = os.path.join(src_path, 'functions')
        if not os.path.exists(functions_path):
            os.makedirs(functions_path)

        scripts_path = os.path.join(src_path, 'scripts')
        if not os.path.exists(scripts_path):
            os.makedirs(scripts_path)

    create_src_subfolders(proj_name)

# Call the function with user given name
proj_name = "a_lesion_QSM_Sh"
create_folder_structure(proj_name)
