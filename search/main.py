from typing import Dict, Union, List, Optional
from search.utils import convert_datetime, check_platform, get_default_path
import os
import pathlib
import time


class Search:
    def __init__(
        self,
        path: str = None,
    ) -> None:
        self._path = path
        self._error_data = []

    def entity_data(self) -> Dict[str, List[Dict[str, str]]]:
        """
        A function which walk through all the files and folders in the given path and return stat and pathlib.Path data
        :return: Dict[str, List[Dict[str, str]]]
        """
        _file_data = []
        _folder_data = []
        for root, folders, files in os.walk(self._path):
            # Getting files info
            for file in files:
                # try:
                entry = pathlib.Path(os.path.join(root, file))
                stat = entry.stat()
                _file_data.append(
                    {
                        "name": entry.name,
                        "type": "File",
                        "suffix": entry.suffix,
                        "path": entry.__str__(),
                        "group": entry.group(),
                        "owner": entry.owner(),
                        "stat": {
                            "st_mode": oct(stat.st_mode & 0o777),
                            "st_uid": stat.st_uid,
                            "st_gid": stat.st_gid,
                            "st_size": stat.st_size,
                            "st_mtime": stat.st_mtime,
                            "st_ctime": stat.st_ctime,
                        },
                    }
                )
            # except PermissionError as pe:
            #     self._error_data.append({"PermissionError": pe.__str__()})
            # except Exception as e:
            #     os.remove(os.path.join(root, file))
            #     self._error_data.append({"Error": e.__str__()})
            # Getting folders info
            for folder in folders:
                # try:
                entry = pathlib.Path(os.path.join(root, folder))
                _folder_data.append(
                    {
                        "name": entry.name,
                        "type": "Folder",
                        "path": entry.__str__(),
                        "group": entry.group(),
                        "owner": entry.owner(),
                        "permission": oct(entry.stat().st_mode & 0o777),
                    }
                )
            # except PermissionError as pe:
            #     self._error_data.append({"PermissionError": pe.__str__()})
            # except Exception as e:
            #     os.rmdir(os.path.join(root, folder))
            #     self._error_data.append({"Error": e.__str__()})

        return {"File": _file_data, "Folder": _folder_data}

    def __str__(self) -> str:
        return f"Path : {self._path}"

    def get_errors(self):
        return self._error_data


class OrdinaryData(Search):
    def __init__(
        self,
        name: Union[str, List[str]] = None,
        group: Union[str, List[str]] = None,
        owner: Union[str, List[str]] = None,
        suffix: Union[str, List[str]] = None,
        type: Optional[str] = None,
        path: Optional[str] = None,
    ) -> None:
        super().__init__(path)
        self._name = name
        self._type = type
        self._path = path
        self._group = group
        self._owner = owner
        self._suffix = suffix
        self._data: dict[str, list[dict[str, str]]] = self.entity_data()

    def clear(self):
        """
        Copy all the file and folder data and clear the source
        :return: dict[str, list[dict[str, str]]] = self._data
        """
        _data = self._data.copy()
        self._data = {"File": [], "Folder": []}
        return _data

    def __str__(self) -> str:
        return f"Name : {self._name}\nType : {self._type}\nPath : {self._path}\nGroup : {self._group}\nOwner : {self._owner}"

    def search_by_name(self) -> None:
        """
        Overwrite and Filter the previous Dict _data with new File and Folder values searched by name
        :return: None
        """
        _data = self.clear()

        # Checking for name type
        if isinstance(self._name, str):
            # Going over files
            for data in _data["File"]:
                if data["name"].__contains__(self._name):
                    self._data["File"].append(data)
            # Going over folders
            for data in _data["Folder"]:
                if data["name"].__contains__(self._name):
                    self._data["Folder"].append(data)
        if isinstance(self._name, list):
            for s_name in self._name:
                # Going over files
                for data in _data["File"]:
                    if data["name"].__contains__(s_name):
                        self._data["File"].append(data)
                # Going over folders
                for data in _data["Folder"]:
                    if data["name"].__contains__(s_name):
                        self._data["Folder"].append(data)

    def current_result_output(self) -> Dict:
        return {"Folder": self._data["Folder"], "File": self._data["File"]}

    def search_by_suffix(self) -> None:
        """
        Overwrite the previous dict source with files searched by suffix
        :return: None
        """
        _data = self.clear()
        # Checking for suffix type
        if isinstance(self._suffix, str):
            for data in _data["File"]:
                if data["suffix"].__eq__(self._suffix):
                    self._data["File"].append(data)
        if isinstance(self._suffix, list):
            for s_suffix in self._suffix:
                for data in _data["File"]:
                    if data["suffix"].__eq__(s_suffix):
                        self._data["Folder"].append(data)

    def search_by_group(self) -> None:
        _data = self.clear()
        # Checking for group type
        if isinstance(self._group, str):
            # Going over files
            for data in _data["File"]:
                if data["group"].__eq__(self._group):
                    self._data["File"].append(data)
            # Going over folders
            for data in _data["Folder"]:
                if data["group"].__eq__(self._group):
                    self._data["Folder"].append(data)
        if isinstance(self._group, list):
            for s_group in self._group:
                # Going over files
                for data in _data["File"]:
                    if data["group"].__eq__(self._group):
                        self._data["File"].append(data)
                # Going over folders
                for data in _data["Folder"]:
                    if data["group"].__eq__(s_group):
                        self._data["Folder"].append(data)

    def search_by_owner(self) -> None:
        """
        Overwrite the previous dict source with files searched by owner
        :return: None
        """
        _data = self.clear()
        # Checking for owner type
        if isinstance(self._owner, str):
            # Going over files
            for data in _data["File"]:
                if data["owner"].__eq__(self._owner):
                    self._data["File"].append(data)
            # Going over folders
            for data in _data["Folder"]:
                if data["owner"].__eq__(self._owner):
                    self._data["Folder"].append(data)
        if isinstance(self._owner, list):
            for s_owner in self._owner:
                # Going over files
                for data in _data["File"]:
                    if data["owner"].__eq__(self._owner):
                        self._data["File"].append(data)
                # Going over folders
                for data in _data["Folder"]:
                    if data["owner"].__eq__(s_owner):
                        self._data["Folder"].append(data)


class FileApi(OrdinaryData):
    def __init__(
        self,
        path: str = get_default_path(check_platform()),
        name: Optional[str] = None,
        type: Optional[str] = None,
        group: Optional[str] = None,
        owner: Optional[str] = None,
        suffix: Optional[str] = None,
        st_mode: Optional[int] = None,
        st_uid: Optional[int] = None,
        st_gid: Optional[int] = None,
        min_st_size: Optional[float] = 0.0,
        max_st_size: Optional[float] = 0.0,
        st_mtime: Optional[str] = None,
        st_ctime: Optional[str] = None,
    ) -> None:

        super().__init__(name, group, owner, suffix, type, path)
        self._path = path
        self._name = name
        self._type = type
        self._group = group
        self._owner = owner
        self._suffix = suffix
        self._st_mode = st_mode
        self._st_uid = st_uid
        self._st_gid = st_gid
        self._min_st_size = float(min_st_size)
        self._max_st_size = float(max_st_size)
        self._st_mtime = convert_datetime(st_mtime)
        self._st_ctime = st_ctime
        self._path = path

    def search_by_st_mode(self):
        _data = self.clear()
        for data in _data["File"]:
            if data["stat"]["st_mode"].__eq__(self._st_mode):
                self._data["File"].append(data)

    def search_by_st_uid(self):
        _data = self.clear()
        for data in _data["File"]:
            if data["stat"]["st_uid"].__eq__(self._st_uid):
                self._data["File"].append(data)

    def search_by_st_gid(self):
        _data = self.clear()
        for data in _data["File"]:
            if data["stat"]["st_gid"].__eq__(self._st_gid):
                self._data["File"].append(data)

    def search_by_st_size(self):
        _data = self.clear()
        for data in _data["File"]:
            if self._min_st_size <= data["stat"]["st_size"] <= self._max_st_size:
                self._data["File"].append(data)

    def search_by_st_mtime(self):
        pass

    def search_by_st_ctime(self):
        pass


# 2.7
instance = FileApi(
    name="gay",
    group="erfan",
    suffix=".py",
)

print(instance._error_data)
print("hello")
