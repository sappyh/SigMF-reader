## SigMF Reader.readme

Python module to read SigMF datasets and categorize them into dataframes.  



![SigMF-reader block digram](https://github.com/sappyh/SigMF-reader/blob/master/SigMF-reader.png)



**SigMF Directory:** Path to the directory holding the SigMF dataset, can hold the dataset in multiple files

**Pandas Dataframe:** The output dataframe object for the entire dataset

### Structure of SigMF Reader

Directory Loader: Enumerates all the SigMF recordings available at the provided path. Checks data consistency of each datafile to each meta datafile. Returns a dictionary of metafile and datafile.

Load metafile: Loads the elements of the metadata so the it can parse and enumerate the metadata contents.

Data Loader: Loads the datafile

Annotation Segmenter: Segments the datafile according to the annotations found in the metafile. Uses core::sample_start and core::sample_count. Further comments such as node id is added as an extra feature in the pandas data row for each annotation

Pandas Exporter: Combines the the segments for each annotated capture from different recording into a single dataframe

### Example

```python
from sigmfreader import sigmfreader
# Define the number of samples in one timeseries training samples
ncols=128
# Define the number of symbols needed
symbol_length=32
# Call the reader
reader=sigmfreader("SigMF_dir", ncols, symbol_length)
# Do the pd exporter
df = reader.pandas_exporter()
# print the dataframe
df.head()
```



### Note:

Not generalized yet to handle all sigMF Json name/values, will keep updating to make it more generalized

