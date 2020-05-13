## Python module for reading sigmf data files
import json
import codecs
import pandas as pd
import numpy as np
from pathlib import Path

SIGMF_METADATA_EXT = ".sigmf-meta"
SIGMF_DATASET_EXT = ".sigmf-data"


class sigmfreader(object):
    #File Dictionary Keys
    METADATA = 0
    DATAFILE = 1
    
    # Set keys
    START_INDEX_KEY = "core:sample_start"
    LENGTH_INDEX_KEY = "core:sample_count"
    START_OFFSET_KEY = "core:offset"
    VERSION_KEY = "core:version"
    GLOBAL_KEY = "global"
    CAPTURE_KEY = "captures"
    ANNOTATION_KEY = "annotations"
    
    # Extension Keys
    NODEID_KEY= "rfbuddy:nodeid"
    
    
    def __init__(self, path, ncols):
        self.path=Path(path)
        self.ncols=ncols
        self.columns=np.array([i for i in range(self.ncols)])
        self.df=pd.DataFrame(columns=self.columns)
    
    def fromdirectory(self):
        dataset=dict()
        recordings= self.path
        for recording in recordings.iterdir():
            if recording.name.endswith(SIGMF_DATASET_EXT):
                assert (recordings.joinpath(recording.stem+SIGMF_METADATA_EXT)).exists() ==True, "Metadata file not found for %s" %recording.name
                dataset[recording.stem]=[recordings.joinpath(recording.stem+SIGMF_METADATA_EXT), recording]
        return dataset
          
    def loadmetafile(self, streamer):
        self.metadata= json.load(streamer)
        self.global_info=self.metadata.get(self.GLOBAL_KEY, None)
        self.capture_info = self.metadata.get(self.CAPTURE_KEY,None)
        self.annotation_info = self.metadata.get(self.ANNOTATION_KEY,None)
        
        
        
    def loaddatafile(self, file):       
        self.datafile= np.fromfile(file, dtype=np.complex64)
 
    def annotator_segmenter(self):
        nodeid= self.global_info.get(self.NODEID_KEY)
        annotated_df= pd.DataFrame(columns=self.columns)
        for i in range(len(self.annotation_info)):
            sample_start= self.annotation_info[i].get(self.START_INDEX_KEY)
            sample_count= self.annotation_info[i].get(self.LENGTH_INDEX_KEY)
            
            
            
            annotated_array=self.datafile[sample_start:(sample_start+ sample_count)]
            
            
            ## Have to pad zeros to make all the rows same in length
            
            N = self.ncols - len(annotated_array)%self.ncols
            annotated_array=np.pad(annotated_array, (0, N), 'constant')
            annotated_array= np.reshape(annotated_array,(-1, self.ncols))
            annotated_df=annotated_df.append(pd.DataFrame(data=annotated_array, dtype=np.complex64),ignore_index=True)
        
        annotated_df["nodeid"]=nodeid
        return annotated_df
    
    def pandas_exporter(self):
        dataset=self.fromdirectory()
        bytestream_reader = codecs.getreader("utf-8")  # bytes -> str
        #Try to load one datafile and one metafile
        keys= list(dataset.keys())
        
        for key in keys:
            print(key)
            self.loadmetafile(bytestream_reader(open(dataset[key][self.METADATA],'rb')))
            self.loaddatafile(dataset[key][self.DATAFILE])
        
            annotated_df= self.annotator_segmenter()
            self.df= self.df.append(annotated_df)
        
#         self.df=self.df.astype(np.complex64)
        
        return self.df