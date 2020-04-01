# Python Appetiser presentation / training

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thiersa/Python-Appetiser/master)

Run this notebook from a conda environment `presentation`.
In this directory type:

```
$ source activate presentation
$ jupyter notebook notebooks/Python-Appetiser.ipynb
```

Please make a copy from the source, because using the notebook will
actually make changes.

To make a pdf from the notebook run thіs command:
```
$ jupyter nbconvert --to slides notebooks/Python-Appetiser.ipynb --allow-errors --reveal-prefix reveal.js --post serve
```
It opens up a webpage in the browser at 
`http://localhost:8000/Python-Appetiser.html#/`.

Replace the trailing `#/` by `?print-pdf` in the above URL.

Save to PDF in Chrome using the print option
- Open the in-browser print dialog (Cmd/Ctrl + P).
- Change the Destination setting to Save as PDF.
- Change the Layout to Landscape.
- Change the Margins to None.
- Enable the Background graphics option.
- Click Save.

To re-create the conda environment, do:
```
$ conda list --export > requirements.txt
$ conda create --name <new_name> --file requirements.txt
```

