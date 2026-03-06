# Boulder

## General Stack

### API (Backend)

- TODO

### Frontend

- [Vue 3](https://vuejs.org/guide/introduction.html) + [Vuetify](https://vuetifyjs.com/en/getting-started/installation/#installation)

- [Typescript](https://www.typescriptlang.org/docs/handbook/typescript-from-scratch.html)

- [Axios](https://github.com/axios/axios)

### Database

- TODO

---

## Development

1. [Set up the `dev`](./bin/README.md) command, or use `docker compose -f docker-compose.development.yml` instead of `dev` in all instructions.

2. In `api/` create `.env.development` file with this content. It must match the config in `docker-compose.development.yml`

   ```bash
   FRONTEND_URL=http://localhost:8080
   ```

3. Go back to the top level directory.

4. Boot the api, web, and db services via `dev up`. This will run the boot pipeline and create the database, run migrations, and run seeds.

5. Stop the api, web, and db services via `ctrl+c` or `dev down` or if you want to wipe the database `dev down -v`.

6. Install local dependencies by running `npm install` at the top level of the project.

7. Install `web` dependencies by running `dev web npm i`

### API Service (a.k.a back-end)

1. Boot only the api service using:

   ```bash
   dev up api

   # or

   docker compose -f docker-compose.development.yml up api

   # or

   ./bin/boot-app.sh # from the /api directory
   ```

2. Access the api by going to <http://localhost:5000>

### Web Service (a.k.a. front-end)

1. Boot only the web service using:

   ```bash
   dev up web

   # or

   docker compose -f docker-compose.development.yml up web

   # or

   npm run start # from the /web directory
   ```

2. Log in to the front-end service at <http://localhost:8080>

### Migrations

TODO

### Seeding

TODO

## Deploying

### VIU Lab Machine Environment

TODO

### Production Environment (remote) (dont need this?)

TODO

### Test Production Build Locally

TODO
