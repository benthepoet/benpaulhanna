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

Now let's scaffold out the most basic use of Backbone with `webpack`. Let's save this file 
as `src/index.js`.

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');

// Execute after the DOM has loaded
Backbone.$(function () {
  // Start Backbone
  Backbone.history.start();
  
  // Display a simple message
  Backbone
    .$('body')
    .text('App Ready');
});
```

With all the base components stubbed out we can now start up the application.

```bash
npm start
```

Navigate to `http://localhost:8080` in a browser and you should see the message displayed.

# Add a View
Displaying a message is neat, but let's expand out the application to utilize a view. For that 
let's create the following as `src/view.js`.

```js
// Import the Backbone module and its dependencies
const Backbone = require('backbone');

// Declare our options we'll use to extend the base view
const viewOptions = {
  el: 'body',
  
  render() {
    this.$el.text('App Ready');
  }
};

// Export our extended view
module.exports = Backbone.View.extend(viewOptions);
```

Back in `src/index.js`, we'll need to import our view module, create an instance, and attach 
it to the DOM.

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');
var AppView = require('./app.view');

// Execute after the DOM has loaded
Backbone.$(function () {
  // Start Backbone
  Backbone.history.start();
  
  // Create an instance of our view
  new AppView();
});
```