import os

class Shell:

    def __init__(self):
        self.cwd: str = '/Users/romero'

    def update_pwd(self):
        """Updates the state of the Shell object"""
        self.cwd = os.getcwd()


    def cd(self,  route: str = '../'):
        """Moves among directories"""

        newpath = os.path.join(self.cwd, route)
        os.chdir(newpath)
        
        self.update_pwd()

    def mkdir(self, name: str) -> None:
        """Creates new directories in cpw"""
        pwd = os.getcwd()
        path = os.path.join(pwd, name)
        os.makedirs( path )

    def ls(self) -> list :
        """Returns a list with the directories/files in cwd"""
        return os.listdir(self.cwd)

    def lsdir(self):
        directories = []
        for element in self.ls():
            if '.' not in element:
                directories.append(element)

        return directories


    def rm(self, name :str, flag: str = '') -> None: 
        """Removes a directory or a file inside cwd"""
        pwd = os.getcwd()
        path = os.path.join (pwd, name)

        if flag == 'r':
            os.rmdir(path)
            return 

        os.remove(path)
