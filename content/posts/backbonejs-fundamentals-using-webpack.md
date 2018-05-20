Title: Backbone.js Fundamentals: Using Webpack
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

## Create the project
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

## Install and configure Webpack

```bash
npm install --save webpack
npm install --save-dev webpack-dev-server
```

Now let's setup a configuration.

## Bootstrapping the application
Before we can load our application we need to create our shell. We'll save this file as 
`app/index.html`.

```html
<!DOCTYPE html>
<html>
    <head>
        <script src="app.js"></script>
    </head>
    <body>
    </body>
</html>
```

Now let's scaffold out the most basic use of Backbone with `webpack`. Let's save this file 
as `app/app.js`.

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');

// Execute after the DOM has loaded
Backbone.$(function () {
    // Create view and routers here

    // Start Backbone
    Backbone.history.start();
});
```