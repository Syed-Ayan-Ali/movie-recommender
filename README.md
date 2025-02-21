# Movie Recommender Project

An open-source movie recommender system built using Node.js, Express, and MongoDB. This project provides a simple API for fetching movie recommendations based on user preferences.

## Technical Stack

- [Node.js](https://nodejs.org/en/download/)
- [Express](https://expressjs.com/)
- [MongoDB](https://www.mongodb.com/)

## Features

- [x] Movie recommendations based on user preferences
- [x] Simple API for fetching recommendations
- [x] Database storage for user preferences and movie data

## Requirements

Before you begin, you need to install the following tools:

- [Node (current LTS version)](https://nodejs.org/en/download/)
- [npm (latest version or > v10)](https://www.npmjs.com/get-npm)
- [Git](https://git-scm.com/downloads)

## Getting started

1. Clone the repository:

```
git clone https://github.com/<your-username>/movie-recommender.git
cd movie-recommender
```

2. Install dependencies:

```
npm install
```

3. Create a `.env` file in the root directory and add your MongoDB connection string:

```
MONGODB_URI=<your-mongodb-connection-string>
```

4. Start the server:

```
npm start
```

The server will start on port 3000. You can change the port in the `package.json` file.

```json
"scripts": {
  "start": "node index.js",
  "build": "tsc",
  "serve": "node dist/index.js",
  "lint": "eslint . --ext .js,.ts",
  "test": "mocha test/**/*.test.js"
}
```

## API Endpoints

- `GET /recommendations`: Returns movie recommendations based on user preferences.

## Testing

To run the test suite, execute the following command:

```
npm test
```

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the [MIT License](LICENSE).

## Additional Resources

- [Node.js](https://nodejs.org/en/docs/)
- [Express](https://expressjs.com/en/4x/api.html)
- [MongoDB](https://docs.mongodb.com/)
- [npm](https://docs.npmjs.com/)
