# Packages System
The package system of the project is very simple, and most often used in the import of settings, for this, the `packages` folder stores .json files of the packages themselves and also many folders with API and other packages, you can also create your own package using a `.json` file or folder.

## Create Package
Creating the first package is very cool, you can post it on our site on the site, or communities with your friends, and you can also use them absolutely free, to create the first package you need to fill in the data:

| Name          | description                     |
|---------------|---------------------------------|
| manifest      | Package names                   |
| version       | Package application version     |
| description   | Package descriptions            |
| author        | Package author                  |
| components    | Package Components              |

A simple package example:
```json
{
    "manifest": "test-package",
    "version": "xx.xx.xx.y",
    "description": "I dont know(((",
    "author": "IDKinc",
    "components": {
        "debug": {
            ...
        },
        "settings": {
            ...
        }
    }
}
```

## Launch Package
To run the package, you just need to transfer it to the packages folder and it will work, also check for errors and also the application version of the package.