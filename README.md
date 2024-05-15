# WoH Mystery Validator
## About
A set of simple Python scripts for modders to quickly validate World of Horror custom mysteries for most common issues

Currently implemented checks:
- unclosed/extra quotation marks
- duplicate keys
- asset and trigger paths
- allowed key values

More checks might be implemented later.

Validating a mystery automatically validates all linked events and enemies, including nested event chains.

It's also possible to validate events and enemies directly, but because of how WoH paths are specified, it requires passing additional arguments to the script.

## Compatibility
This tool is currently compatible with World of Horror 1.01 (live public Steam release)

## Usage:
### Simple
(Windows only)

Download validate.exe from releases tab, drag & drop your main mystery .ito file on it. Results with be displayed in terminal.

### Advanced
(Requires Python 3.6 or higher)
#### Validating a mystery
```
python validate_mystery.py .\my_mysteries_directory\mystery.ito
```
#### Validating a normal event
```
python validate_event.py .\my_events_directory\event.ito
```

####  Validating a mystery event, assuming your main mystery .ito is in .\my_mysteries_directory
```
python validate_event.py .\my_mysteries_directory\sub_directory\mystery_event.ito --mod_dir mystery\ --mod_root .\my_mysteries_directory
```

####  Building executable with pyinstaller
```
pyinstaller --onefile --add-data "scripts;scripts" --add-data "config;config" validate.py
```

## Credits
https://github.com/Myonmu/WoH-Community-Modding-Guide was used as a main source of info on .ito layout and available values.
