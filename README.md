# SekurPad-API

SekurPad is a prototype of an alternative to number pad. The idea is based on modifiers applied to a PIN in order to make the process of entering the PIN more secure from thermal, smudge and shoulder peek attacks.

The API is hosted at <https://sekurpad-api.herokuapp.com>. The API only uses two basic end-points:

POST `"https://sekurpad-api.herokuapp.com/api/logs"` - create a log entry

Example request body:

```json
{
    "userUuid":"example",
    "timestamp":"21/20/1971",
    "activity":"started"
}
```

GET `"https://sekurpad-api.herokuapp.com/api/logs"` - get all log entries (no body)

## Installing dependencies

Make sure you have nodejs and npm installed then run `npm install` from the directory containing `package.json`.

## Running the API

The API can be run by using node - `node index.js` from the directory containing `index.js`.

Alternately you can [use docker to run the API as a container](https://docs.docker.com/get-started/02_our_app/) with the provided `Dockerfile`.
