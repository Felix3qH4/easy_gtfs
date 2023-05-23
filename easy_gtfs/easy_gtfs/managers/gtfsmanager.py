"""
    This class handles all the other managers (altough they each work on their own).
    You can use this class to quickly read a gtfs dataset or create one from your data without calling each single manager by hand.
"""

import os
from zipfile import ZipFile


from ..utility import get_error_manager
from ..variables import FILES, OUTPUT_FOLDER
from .agencymanager import Agencies
from .stopmanager import Stops
from ..models.errors import ErrorTypes, GTFSError


"""
    TODO: Need to check if stop id in route corresponds to an actual stop in stops.txt, same for agency id and other ids
"""

class GTFSManager():
    def __init__(self, silent_errors: bool = False) -> None:
        self.silent_errors = silent_errors
        self.error_manager = get_error_manager()
        self.error_manager.set_silent_errors(self.silent_errors)
        
            

    def load_folder(self, input_folder: str, is_zip: bool = True, output_folder: str = None) -> dict:
        """
            Loads a folder adhering to the gtfs standards.

            :param input_folder [str] -- The path to the input folder
            :param is_zip [Optional[bool]] -- If the provided folder is a zip folder or not (default=True)
            :param output_folder [Optional[str]] -- The path to the folder into which the files will be extracted if you provide a zip folder

        """

        data: dict = {}
        
        if is_zip:
            #utf8_reader = codecs.getreader("utf-8")
            
            with ZipFile(input_folder, "r") as folder:
                if output_folder == None:
                    output_folder = str(str(os.getcwd()) + OUTPUT_FOLDER + "/" + str(".".join(input_folder.split(".")[:-1]))) # Returns the name of the folder without the ending (could also do input_folder.replace(".zip", "") )
                    
                folder.extractall(path = output_folder)
                
            
            self.load_folder(input_folder = output_folder, is_zip=False)
                #for file in folder.namelist():
                    #with folder.open(file, "r") as _file:
                        #a = utf8_reader(_file) or:
                        #a = io.StringIO(_file.read().decode())
                        #data[file] = list(csv.DictReader(a))

                        #self.parse_DictReader(data[file])

        if not is_zip:
            data["folder"] = str(input_folder)

            for file in list(os.listdir(input_folder)):
                filepath = str(input_folder + "/" + file)
                file_lower = str(file).lower()

                if file_lower == "agency.txt":
                    ag = Agencies()
                    data["agency"] = ag.load_file(filepath) 

                elif file_lower == "stops.txt":
                    st = Stops()
                    data["stops"] = st.load_file(filepath)

                else:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(GTFSError(
                            error_type=ErrorTypes.GTFSErrorUnknownFile,
                            message="Unknown file in dataset.",
                            values = [filepath]
                        ))
                    else:
                        raise ValueError(f"Unknown file in dataset: {filepath}")


        return data
    

    def save_to_folder(self, data: dict, output_folder: str, skip_unknown: True) -> bool:
        """
            Saves data adhering to the gtfs standards to a folder.

            :param data [dict] -- The gtfs data to write to the folder
            :param output_folder [Optional[str]] -- The path to the output folder (it will not create a new folder in the folder you pass)
            :param skip_unknown [Optional[bool]] -- Skip unknown keys

            :return [bool] -- True on success, False on fail
        """

        for _key in data:
            key_lower = str(_key).lower()

            ## Agencies
            if key_lower == "agency":
                file = str(output_folder + "/agency.txt")
                cl = Agencies()
                success = cl.to_file(data[_key], file=file)

                if not success:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(GTFSError(
                            error_type=ErrorTypes.GTFSErrorProcessReturnedFalse,
                            message = "'Agencies().to_file()' returned False upon execution. (Maybe check previous errors?)",
                            values = [file, data[_key]]
                        ))
                    else:
                        raise InterruptedError(f"Process interrupted while saving file: {file} \n Function 'Agencies().to_file()' did not return True upon execution. (Check silent errors log?) \n Data: {data[_key]}")
                    
            ## Stops
            elif key_lower == "stops":
                file = str(output_folder + "/stops.txt")
                cl = Stops()
                success = cl.to_file(data[_key], file=file)

                if not success:
                    if self.error_manager.is_silent_errors():
                        self.error_manager.add_error(GTFSError(
                            error_type=ErrorTypes.GTFSErrorProcessReturnedFalse,
                            message = "'Stops().to_file()' returned False upon execution. (Maybe check previous errors?)",
                            values = [file, data[_key]]
                        ))
                    else:
                        raise InterruptedError(f"Process interrupted while saving file: {file} \n Function 'Stops().to_file()' did not return True upon execution. (Check silent errors log?) \n Data: {data[_key]}")
                
