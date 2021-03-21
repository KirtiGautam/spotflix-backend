## Spotflix

## How to run:
- Clone the repository
- CD to the local repository.
- Copy the docker-compose.yml.template to same directory and rename it to docker-compose.yml
- Mention the variables in the docker-compose.yml file
- Download docker for your system.
- Build docker images

    ```
    docker-compose build api
    ```

- Run docker containers

    ```
    docker-compose up -d db api
    ```

- The database can be accessed by this command, on password prompt type `postgres`

    ```
    docker-compose run db psql -h db -U postgres spotflix
    ```

- To tail the logs a service you can do
    
    ```
    docker-compose logs -f <api / db>
    ```

- To stop the containers

    ```
    docker-compose stop api api
    ```

- To restart any containers 

    ```
    docker-compose restart api
    ```

- To run bash inside any container for purpose of debugging do

    ```
    docker-compose exec api /bin/bash
    ```


## Development Guide:
- Create a branch and make your changes and push to your branch.
- Do not push to master.
- All the changes will be merged from your branch.