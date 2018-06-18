Title: Native HTML5 Drag and Drop with Elm
Category: Blog
Date: 05-21-2018 22:50:00
Series: Practical Elm
Status: draft

In doing some research for a potential project I decided to see how drag and drop 
functionality can be implemented in Elm.

Thankfully, it looks like it's not too hard to achieve since drag and drop is now 
part of the HTML5 standard.

With that said I'm going to construct an application that allows you to add build 
a list by dragging an element one or more times onto the list. We'll start with a 
`beginnerProgram` since it doesn't look like we'll need `init` or `subscriptions`.

```elm
import Html
```