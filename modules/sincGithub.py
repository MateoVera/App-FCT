from github import Github
import streamlit as st
import os

def sincronizar_bd_con_github():
    token = st.secrets['github_token']
    repo_name = st.secrets['github_repo']
    branch = 'main'
    
    ruta_bd_local = st.session_state.get('bdActual')
    if not ruta_bd_local or not os.path.exists(ruta_bd_local):
        return
        
    nombre_archivo_github = os.path.basename(ruta_bd_local)

    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        with open(ruta_bd_local, 'rb') as f:
            contenido_nuevo = f.read()
        
        try:
            contents = repo.get_contents(nombre_archivo_github, ref = branch)
            
            repo.update_file(
                path = contents.path,
                message = 'Auto-guardado: Actualizacion de la base de datos',
                content = contenido_nuevo,
                sha = contents.sha,
                branch = branch
            )
        except Exception:
            repo.create_file(
                path = nombre_archivo_github,
                message = f'Auto-guardado: Creacion de la base de datos {nombre_archivo_github}',
                content = contenido_nuevo,
                branch = branch
            )
    except Exception as e:
        st.error(f'Error de sincronizacion: {e}')

def eliminar_bd_en_github(nombre_archivo):
    token = st.secrets['github_token']
    repo_name = st.secrets['github_repo']
    branch = 'main'
    
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        contents = repo.get_contents(nombre_archivo, ref = branch)
        
        repo.delete_file(
            path = contents.path,
            message = f'Auto-guardado: Eliminacion de la base de datos {nombre_archivo}',
            sha = contents.sha,
            branch = branch
        )
    except Exception as e:
        st.error(f'Error al eliminar en GitHub: {e}')

def sincronizar_config_con_github():
    token = st.secrets['github_token']
    repo_name = st.secrets['github_repo']
    branch = 'main'
    
    directorioBase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_txt = os.path.join(directorioBase, '.app_config.txt')
    
    if not os.path.exists(ruta_txt):
        return
        
    nombre_archivo_github = '.app_config.txt'
    
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        with open(ruta_txt, 'r', encoding = 'utf-8') as f:
            contenido_nuevo = f.read()
        
        try:
            contents = repo.get_contents(nombre_archivo_github, ref = branch)
            if contents.decoded_content.decode('utf-8') != contenido_nuevo:
                repo.update_file(
                    path = contents.path,
                    message = 'Auto-guardado: Actualizacion de configuracion .txt',
                    content = contenido_nuevo,
                    sha = contents.sha,
                    branch = branch
                )
        except Exception:
            repo.create_file(
                path = nombre_archivo_github,
                message = 'Auto-guardado: Creacion de configuracion .txt',
                content = contenido_nuevo,
                branch = branch
            )
    except Exception:
        pass