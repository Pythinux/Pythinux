import importlib
def import_library(library_name,library_version):
    ## Check library is valid
    if os.path.isdir(f"lib/{library_name}/{library_version}"):
        os.chdir(f"lib/{library_name}/{library_version}")
        return importlib.import_module(library_name)
    else:
        raise OSError("Invalid library: '{}' {}.".format(library_name, library_version))
if __name__ == "__main__":    
    print("LibImporter is designed to be used by other programs.")
    print("To import libimporter into a Pythinux app (running in app_high):")
    print("libimporter = silent(lambda:load_program('libimporter',user))")
    print("To import a library:")
    print("pythinux.libimporter.import_library(lambda:'library','1.0.0')")
