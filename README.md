# truck-api
```
This is a sample of an serverless service hosted by AWS.
In this project, we aim to keep track of truck drivers which come and go from terminals.
```


# Installation
```
This project requires an AWS account and python 3.8 or newer to work.
```

## Serverless
```
First, Download and Install NPM which will manage our serverless instance.
Then, run serverless and follow the instruction to create the basic configuration files.
In order to deploy the project on AWS, you must have an account and have a AWS Key and Secret.
With this in hand, add your keys to the configuration.
```
```
sudo apt-get install npm 
sudo npm install -g serverless
serverless config credentials --provider aws --key AWS_KEY --secret AWS_SECRET
serverless
```

### Plugins
```
This applications require some plugins in order to work. 
First we initiate NPM to make a 'package' file whick will manage the plugins of our serverless application
Then, install the 'requirements' and 'dotenv' plugins. These will tell the Cloudformation the Python requirements and
Enviroment Variables needed to be loaded.
```
```
npm init
sudo npm install -g serverless-python-requirements serverless-dotenv-plugin
```
## Python Packages
```
This application will copy the requirements installed in the current enviroment to the project.
So, we must install all the requirements written on the file.
```
```
pip -r install requirements.txt
```

# AWS Deployment
```
Then you are ready to deploy.
```
```
serverless config credentials --provider aws --key AWS_KEY --secret AWS_SECRET
sls deploy
```

```
This will make a CloudFormation containing all the project assets such as Lambda, S3, API Gateway, etc
```

# Endpoints
```
I've set up a demo that can be accessed for the next 2 weeks:
https://j0tg1td581.execute-api.us-east-1.amazonaws.com/dev
```
## Users data
**GET     /users**
```
Description: List all users(drivers) who pass through a terminal
QueryString:
-name: Name of user
type: string
-gender: Gender of user. "m" for male and "f" for females
type: char
-ownVehicle: If the user has its own vehicle
type: bool
-licence: Driver's licence (CNH) category. As for Brazilian standards, they go from "a" to "e"
type: char
```
**POST    /users**
```
Description: Creates a new user
Parameters:
-body(required): Dictionary containing all the user information (name, gender, age, ownVehicle, licence)
type: body
```

**GET     /users/{user_id}**
```
Description: Get the data from a specific user
Parameters:
-user_id(required): Id of user.
type: int
```

**PUT     /users/{user_id}**
```
Description: Update(changes) the data from a specific user
Parameters:
-user_id(required): Id of user.
type: int
-body(required): Dictionary containing one or more user information (name, gender, age, ownVehicle, licence)
type: body
```

## Terminals data


**GET     /terminals/{terminal_id}**
```
Description: List all traffic of incomming drivers. Without time query, it return the last day data
Parameters:
-terminal_id(required): Id of user.
type: int
QueryString:
-ini_date: Initial date for query. format: "%Y-%m-%d %H:%M"
type: string
-end_date: Final date for query.format: "%Y-%m-%d %H:%M"
type: string
-loaded: If True, return only users with loaded trucks. False return all data
type: bool
-groupByVehicle: If True,return all traffic grouped by type of Vehicle.  False return all data
type: bool
```

**POST    /terminals/{terminal_id}**
```
Description: Adds a new traffic info.
Parameters:
-body(required): Dictionary containing all the traffic information (user_id, origin, destination, loaded, vehicle)
type: body
```

# Database Structure
```
S3_BUCKET
└───users
|   └───user_list.json
└───terminals
    └───<id>
        └───Datalake_Structure(%Y/%m)
            └─── terminal_<id>_%Y%m%d.json
```
