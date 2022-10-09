import hashlib
import os
from rich import print
from rich.table import Table
from rich.console import Console
import fire

BUF_SIZE = 524288

def sha256(file):
    """Calculates a SHA256 hash of a file.
    
    The passed file arguments has to be a path to a file.
    Return the hash of the file
    """
    console = Console()
    with console.status("[bold green] Calculating hash...") as status:
        sha256 = hashlib.sha256()
        file_size = os.path.getsize(file)
        with open(file, 'rb') as f:
            current=0
            while True:
                data = f.read(BUF_SIZE)
                current += BUF_SIZE
                if not data:
                    break
                sha256.update(data)
                status.update(f"[bold green] Calculating hash...[/bold green][cyan]{file}[/cyan]:{current/1024/1024}/{file_size/1024/1024} MB")
        return sha256.hexdigest()

def get_filelist(dir):
    """Returns the files of a dir
    """
    dir_files = []
    for file in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,file)):
            dir_files.append(file)
    return dir_files

def check_file_presence(dir1,dir2):
    """Returns lists of files which are present in the given directory.

    Return
    -------
    List - Files which are present in both directories
    List - Files which are only present in dir1
    List - Files which are only present in dir2
    """
    same_names = []
    only_dir1 = []
    only_dir2 = []

    dir1_files = get_filelist(dir1)
    dir2_files = get_filelist(dir2)
    for file1 in dir1_files:
        found = False
        for file2 in dir2_files:
            if file1 == file2:
                same_names.append(file1)
                found=True
                break
        if not found:
            only_dir1.append(file1)

    for file2 in dir2_files:
        found = False
        for file1 in dir1_files:
            if file2 == file1:
                found=True
                break
        if not found:
            only_dir2.append(file2)

    return same_names, only_dir1, only_dir2

def compare_dir(dir1,dir2):
    """Compares two directories. Creates hashes for every file in each dir. If two filenames are equal the fileshashes are compared.
    
    This method can be used for backups or grandscale folderwise comparision of hashes.
     """
    #configuring table
    tab = Table(title="Hash[SHA(256)]")
    tab.add_column("File", style="yellow", no_wrap=True)
    tab.add_column(f"Sha-256({dir1})", style="cyan")
    tab.add_column(f"Sha-256({dir2})", style="cyan")
    tab.add_column("Equal", style="cyan")
    
    same_names,only_dir1, only_dir2 = check_file_presence(dir1,dir2)        

    for file in same_names:
        comp = compare_files(os.path.join(dir1,file), os.path.join(dir2,file))
        if comp:
            tab.add_row(file,
                        sha256(os.path.join(dir1,file)),
                        sha256(os.path.join(dir2,file)),
                        "✅")
        else:
            tab.add_row(file,
                        sha256(os.path.join(dir1,file)),
                        sha256(os.path.join(dir2,file)),
                        "❌") 
    for file in only_dir1:
        tab.add_row(file,
                    sha256(os.path.join(dir1,file)),
                    "-",
                    "◀")
    for file in only_dir2:
        tab.add_row(file,
                    "-",
                    sha256(os.path.join(dir2,file)),
                    "▶")
          
    print(tab)
    print()
    print(f"[bold underline]Legend")
    print(f"✅ = Hashes are the same. Files are identical.")
    print(f"❌ = Hashes are different. Files are different. Maybe corrupt ")
    print(f"◀ = File only in dir1")
    print(f"▶ = File only in dir2")

def dir_hash(dir):
    """ Calculates the hashes of the files of the given dir
    """
    #configuring table
    tab = Table(title="Hash[SHA(256)]")
    tab.add_column("File", style="yellow", no_wrap=True)
    tab.add_column(f"Sha-256({dir})", style="cyan")

    files = get_filelist(dir)
    for file in files:
        tab.add_row(file,sha256(os.path.join(dir,file)))
    print(tab)

def compare_files(file1,file2):
    """Compares the SHA256 hash of two files
    
    The file argument has to be a path to a file.
    Returns true if the hash is the same. Otherwise false.
    """
    hash1 = sha256(file1)
    hash2 = sha256(file2)
    if hash1 == hash2:
        return True
    else:
        return False

if __name__ == "__main__":
    fire.Fire()

