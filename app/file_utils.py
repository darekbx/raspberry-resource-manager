from app import app
from os.path import expanduser
from flask import send_file
import os, stat, shutil

class FileUtils():


   
    app_directory = expanduser("~") + app.config['RESOURCES-DIRECTORY'] + '/'
    app_directory_def = expanduser("~") + app.config['RESOURCES-DIRECTORY'] + '/'

    #returns file size in readable format, input
    @staticmethod
    def sizeof_fmt(file_size, suffix='B'):
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(file_size) < 1024.0:
                return "%3.1f%s%s" % (file_size, unit, suffix)
            file_size /= 1024.0
        return "%.1f%s%s" % (file_size, 'Yi', suffix)
    
    def resource_directory(self):
        return self.app_directory
    
    def file_full_path(self, filename):
        return os.path.join(self.resource_directory(), filename)

    def download_file(self, filename):
        file_to_download = self.file_full_path(filename)
        return send_file(file_to_download, as_attachment=True)

    def delete_item(self, filename):
        file_to_remove = self.file_full_path(filename)
        is_file = os.path.isfile(file_to_remove)
        if is_file:
            os.chmod(file_to_remove, stat.S_IWRITE)
            os.remove(file_to_remove)
        else:
            dir_to_remove = file_to_remove
            files_in_directory_to_remove = os.listdir(dir_to_remove)

            for file_chmod in files_in_directory_to_remove:
                os.chmod(dir_to_remove + '/' + file_chmod, stat.S_IWRITE)
            shutil.rmtree(dir_to_remove, ignore_errors=False)
