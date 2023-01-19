# Getting Started with KomeCode
In this section, I will show you and tell you all the most important things to get started, about downloading and setting up the application, as well as about building a project for your device.

## Installing
Downloading the project is very simple, all you need is 3 steps, after that you will be able to set up your project and your applications completely on your own or together with us, namely me, I'm a Guide by the way, for installing we need:

* Installing the project requires downloading a `.zip` archive to your device.
* Go to the developer console and see `cd path-folder`
* Enter this command `pip install -r requirements.txt` to download the necessary modules for the editor to work correctly.

> You must have [Python version 3.1](https://www.python.org/download/releases/3.1/) installed on your device, you must also remember that this is `Python`

Congratulations, you have successfully downloaded our editor to your device!

## Launch Project
Starting a project is very simple, all you need to do is run one `Python` file. We are already in the directory, we will write `cd path-folder`, which means we can run a project that is configured for us, you just need to enter `python setup.py`

## Build Project
To build the project, you need to enter 2 commands, while `pyinstaller` should already be downloaded, here are the 2 commands themselves, along with downloading this module:
```
pip install pyinstaller

pyinstaller -F setup.py
```

## Settings Setup
Setting up the project is very simple and at the same time difficult because the project has a lot of settings files, also language settings, you can change them and also create your own, namely packages, you also have to carefully look at the version of the package, each version has its own architecture, everything can change and be added, but it rarely leads to errors, because of our `Packet-Manager`, which edits everything for you.

| Files name    | Function                        |
|---------------|---------------------------------|
| theme.json    | Color Theme Customization File  |
| settings.json | Main settings file              |
| keys.json     | Customizing application hotkeys |
| debug.json    | Code Run Setting                |
| lang.json     | Language settings               |