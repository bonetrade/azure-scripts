# azure-scripts

See the [section on getting set up with azure](https://shawngraham.github.io/dhmuse/detecting-handwriting/#a-shortcut) to get your Azure credentials; these need to be put in at xxxx and yyyy in lines 80, 81.

These scripts are for working with local files. When it asks you for the file path, make sure to have the trailing slash. Writes results to a txt file, and to the terminal. 

'handwriting' will recognize handwriting in images.
'tags' will identify the likely tags that describe an image.

Python 3. 

Make sure to get the azure sdk first, with

`$ pip install --upgrade azure-cognitiveservices-vision-computervision`
