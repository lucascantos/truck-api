# truck-api
```
This is a sample of an serverless service hosted by AWS.
In this project, we aim to keep track of truck drivers which come and go from terminals.
```


# Installation
```
This project requires an AWS account and python 3.8 or newer
```

## Serverless

```
sudo apt-get install npm
npm install serverless
serverless
```

### Plugins
```
npm init
sudo npm install -g serverless-python-requirements serverless-dotenv-plugin
```
## Python Packages
```
pip -r install requirements.txt
```

# AWS Deployment
```
serverless config credentials --provider aws --key AWS_KEY --secret AWS_SECRET
sls deploy
```

# Endpoints
I've set up a demo that can be used in the next 2 weeks just in case: \n
[https://j0tg1td581.execute-api.us-east-1.amazonaws.com/dev]
## Users data
**GET     /users**
```
Description: List all users(drivers) who pass throgh a terminal
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
Parameters:
-terminal_id(required): Id of user.
type: int
QueryString:
-ini_date
type: string
-end_date
type: string
-loaded: Name of user
type: string
-groupByVehicle
type: bool
```

**POST    /terminals/{terminal_id}**
```
Parameters:
-terminal_id(required): Id of user.
type: int
QueryString:
-name: Name of user
type: string
```

# Database Structure
S3_BUCKET
└───users
|   └───user_list.json
└───terminals
    └───<id>
        └───Datalake_Structure(%Y/%m)
            └─── terminal_<id>_%Y%m%d.json
