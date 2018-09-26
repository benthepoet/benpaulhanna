Title: Building an Elm project with Parcel
Category: Blog
Date: 09-26-2018 08:28:00
Modified: 09-26-2018 08:28:00
Series: Practical Elm

Do you loathe setting up the same `webpack` configuration for every new `elm` project 
you start? Well, worry no more because `parcel`, a zero-configuration bundler, now 
officially supports `elm` assets.

In this tutorial we'll setup a new project from scratch to demonstrate just how easy the process is.

# Create the project
Starting from scratch let's first create a new folder and initialize `npm`.

```bash
mkdir my-elm-app
cd my-elm-app
npm init
```

Next let's install `parcel`. Note this is only dependency we'll explicitly have to install. Development 
dependencies like `elm` and `node-elm-compiler` will automatically be added to your `package.json` when you 
run `parcel`.

```bash
npm install --save parcel
```

Let's create a new folder where we'll place all our source files (HTML, CSS, JavaScript, Elm).

```bash
mkdir src
```

The first file we'll create is `src/index.html`. This will serve as our entry point for the bundler. When run, `parcel`
will automatically resolve any dependencies contained within.

```html
<!DOCTYPE html>
<html>
  <head>
    <script defer src="main.js"></script>
  </head>
  <body>
    <main></main>
  </body>
</html>
```

Next let's create a simple Elm application and save it as `src/Main.elm`.

```elm
import Html

main =
  Html.text "Hello World"
```

And lastly we'll create `src/main.js` which is responsible for pulling in and initializing our Elm application.

```javascript
const { Elm } = require('./Main.elm');

Elm.Main.init({
  node: document.querySelector('main')
});
```

# Serving for development

Now that all our files are in place, serving the project for development is quite easy.

```bash
npx parcel src/index.html
```

Then just navigate to the address presented in the terminal and you should see `Hello World` displayed.

The initial load will take a little longer as it will install the dependencies for `elm` and also initialize the `elm.json` file.
Once it's up and running, you can make changes to any of the source files and the bundle will automatically be rebuilt.

# Building for production

When you're ready to build the application for production all you do is run the following.

```bash
npx parcel build src/index.html
```

Upon completion, the compiled production assets can be found in the `dist` folder.

# Wrapping up

Hopefully this article gave you a good overview on how to use `parcel` with `elm`. The complete code for this tutorial is 
available at my [elm-parcel-example](https://github.com/benthepoet/elm-parcel-example) repository.
