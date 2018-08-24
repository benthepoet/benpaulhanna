Title: Building a Backbone.js project with Parcel
Category: Blog
Date: 08-24-2018 08:26:00
Series: Backbone.js Fundamentals

Do you loathe configuring `webpack` every time you setup a new application? Well, you may be 
better served by `parcel`, an alternative bundler that touts zero-configuration. Quite simply, 
it just works.

In this article I'll demonstrate how setup a basic Backbone project using `parcel`.

# Create the project
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

* `src` - This is where we'll put all our JavaScript, HTML, and CSS.

# Install Parcel
Since the main advantage of `parcel` is that it requires zero-configuration all we really 
need to do use it is install `parcel-bundler`.

```bash
npm install --save parcel-bundler
```

`parcel` performs both the functions of building your bundle and then watching it for changes 
while serving it on a local HTTP server. The latter is similar to what is provided when using 
`webpack-dev-server` with `webpack`.

When you run `parcel` you just tell it what your entry file is (usually `index.html`) and then 
it will automatically find any assets (i.e. scripts, stylesheets) that you're using and bundle them all together.

# Create an application
Before we can load our application we need to create our shell. We'll save this file as 
`src/index.html`.

```html
<!DOCTYPE html>

<html>
  <head>
    <!-- Using the 'async' attribute will keep our script from blocking the page load. -->
    <script src="index.js" async></script>
  </head>
  <body>
  </body>
</html>
```

Now let's scaffold out a basic use of Backbone with `parcel`. 

First we'll create a view for our application in `src/app.view.js`;

```js
// Import the Backbone module and its dependencies
var Backbone = require('backbone');

// Declare our options we'll use to extend the base view
var viewOptions = {
  el: 'body',
  
  initialize: function () {
    this.render();
  },
  
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
npx parcel src/index.html --port 8080
```

Navigate to `http://localhost:8080` in a browser and you should see the message displayed.

# Wrapping up

Hopefully this article demonstrated how easy it is to use `parcel` with Backbone. If 
you'd like to see a slightly more involved example with routing and templates then please see my 
[backbone-fundamentals-parcel](https://github.com/benthepoet/backbone-fundamentals-parcel) 
repository.
