# utils
import tempfile
import yaml



def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        cfg = f.read()
        return yaml.load(cfg,Loader=yaml.FullLoader) 




def save_uploaded_video(uploadedfile):
    with open(uploadedfile.name,"wb") as f:
        f.write(uploadedfile.getbuffer())
    return uploadedfile.name

def save_temp_file(uploadedfile):
    tfile = tempfile.NamedTemporaryFile()
    tfile.write(uploadedfile.read())
    return tfile.name


