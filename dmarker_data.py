import os
import fileinput
import dmarker_config as config
from Marker import Marker

class DataOperation:
    data_file_name = config.data_file_name
    
    @classmethod
    def save_markers(self, marker: Marker):
    # マーカー重複時の削除のロジックを描くのが面倒だったので、
    # ひとまずデータ全体を引っ張ってきて、そこから重複していたら削除or上書きをして、
    # そのデータを用いてデータファイル全てを上書きし直している。
        existing_makers = self.get_markers()        
        existing_makers.append(marker)
        saved_markers = existing_makers
            
        with open(self.data_file_name, mode="w") as data_file:
            for marker in saved_markers:
                data_file.write("{}:{}\n".format(marker.name, marker.path_string))
            data_file.flush()
            os.fsync(data_file)
    
    @classmethod
    def delete_marker(self, marker_name: str):
        markers = self.get_markers()
        for m in markers:
            if m.name == marker_name:
                markers.remove(m)
        
        with open(self.data_file_name, mode="w") as data_file:
            for m in markers:
                data_file.write("{}:{}\n".format(m.name, m.path_string))
            data_file.flush()
            os.fsync(data_file)

    @classmethod
    def get_markers(self) -> list[Marker]:
        if not os.path.exists(self.data_file_name):
            return []

        markers = []
        for line in fileinput.input(files=self.data_file_name):
            data = line.split(":")
            markers.append(Marker(data[0], data[1]))
        return markers
