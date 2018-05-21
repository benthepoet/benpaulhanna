Title: Building a Backbone.js Project with Webpack
Category: Blog
Date: 05-14-2018 08:34:00
Series: Backbone.js Fundamentals
Status: draft

Have you ever wanted to write Backbone.js in the same module format as Node.js? Well here's how 
you can do it with `webpack`.

In short `webpack` allows you to write browser JavaScript using the CommonJS module format. 
The main benefit to this is that `webpack` will bundle all your modules together in a single file 
so that you don't need to manually manage `<script>` tags. And on top of that you can require NPM packages 
as you would in a Node.js application.

# Create the Project
Starting from scratch let's first create a new folder and initialize `npm`.

```bash
mkdir my-backbone-app
cd my-backbone-app
npm init
```

Next let's install `backbone` and it's dependencies, which are `jquery` and `underscore`.

```bash
npm install --save backbone jquery underscore
```

We're going to use the following folder structure.

* `src` - This is where we'll put all our JavaScript.
* `public` - This where we'll put any static files (index.html, assets).

# Install and Configure Webpack
We'll install `webpack` along with `webpack-dev-server`. The latter allows you 
to run a local web server that will also watch your source files for changes.

```bash
npm install --save webpack webpack-cli
npm install --save-dev webpack-dev-server
```

Now let's setup a basic configuration in `webpack.config.js`.

```js
const { resolve } = require('path');

const PUBLIC_PATH = resolve(__dirname, 'public');
const SRC_PATH = resolve(__dirname, 'src');

module.exports = {
  entry: `${SRC_PATH}/index.js`,
  output: {
    filename: 'bundle.js',
    path: PUBLIC_PATH
  },
  module: {
    rules: [
      {
        test: /\.(js)$/,
        exclude: /node_modules/
      }
    ]
  },
  devServer: {
    contentBase: PUBLIC_PATH,
    disableHostCheck: true
  }
};
```

# Create an Application
Before we can load our application we need to create our shell. We'll save this file as 
`public/index.html`.

```html
<!DOCTYPE html>

<html>
  <head>
    <!-- Using the 'async' attribute will keep our script from blocking the page load. -->
    <script src="app.js" async></script>
  </head>
  <body>
  </body>
</html>
```

Now let's scaffold out a basic use of Backbone with `webpack`. 

First we'll create a view for our application in `src/app.view.js`;

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');

// Declare our options we'll use to extend the base view
var viewOptions = {
  el: 'body',
  
  render: function () {
    this.$el.text('App Ready');
  }
};

// Export our extended view
module.exports = Backbone.View.extend(viewOptions);
```

Now let's create our entry module that bootstraps the application at `src/index.js`.

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');

// Import our view
var AppView = require('./app.view');

// Execute after the DOM has loaded
Backbone.$(function () {
  // Create an instance of our view
  new AppView();
});
```

With all the base components stubbed out we can now start up the application.

```bash
npm start
```

Navigate to `http://localhost:8080` in a browser and you should see the message displayed.

Hopefully this article gave you a good overview on how to use `webpack` with Backbone. If 
you'd like to see a slightly more involved example with routing and templates then please see my 
[backbone-fundamentals-webpack](https://github.com/benthepoet/backbone-fundamentals-webpack) 
repository.
