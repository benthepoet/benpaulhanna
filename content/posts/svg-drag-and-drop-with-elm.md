Title: SVG Drag and Drop with Elm
Category: Blog
Date: 08-24-2018 15:13:00
Modified: 08-24-2018 15:13:00
Series: Practical Elm
Status: draft

To follow along with this tutorial I recommend building an application with [Ellie](https://ellie-app.com).

In this article I'll demonstrate how you can implement drag and drop with SVG documents in Elm.

# Getting Started
To start things off let's begin with an empty `Browser.sandbox`. We'll also need to install the `elm/json` and `elm/svg` packages.

```elm
module Main exposing (main)

import Browser
import Svg exposing (Svg)
import Svg.Attributes as Attributes


type Msg
    = NoOp


initialModel = ()


update : Msg -> Model -> Model
update msg model = 
    model


view : Model -> Svg Msg
view model =
    Svg.svg 
        [ Attributes.width "320" 
        , Attributes.height "240"
        ]
        []


main : Program () Model Msg
main =
    Browser.sandbox
        { init = initialModel
        , update = update
        , view = view
        }
```

Add a little bit of CSS so that we can actually see the boundaries of our `svg` element.

```css
svg {
    background-color: #eee;
    border: 2px solid #000;
}
```

At this we have our blank canvas and now we can start the real work.

# Structuring our data
So before we get into the logic of the program, let's define what our model is going to look like.

```elm
type alias Document =
    { width : Int
    , height : Int
    }


type Pointer 
    = Dragging
        { index : Int
        , dx : Int
        , dy : Int
        }
    | Idle


type Shape
    = Circle
        { cx : Int
        , cy : Int
        , r : Int
        , fill : String
        }


type alias Model =
    { document : Document
    , pointer : Pointer
    , shapes : Array Shape
    }
```

We now have three key properties on our model.

* `document` - Specifies the dimensions of our `<svg>` element.
* `pointer` - Used to track when we're dragging a shape.
* `shapes` - A collection of shapes that are contained in the document.

For the sake of simplicity we only have one type of shape, but in the end it'll
be fairly trivial to add any ones.

# Add update messages
Let's define a few messages that we'll use in our `update` function.

```elm
type Msg
    = MouseDown Int Int Int
    | MouseMove Int Int
    | MouseUp
```

Here's how we going to handle each of the messages.

* `MouseDown Int Int Int` - This will fire when we click on a shape to start dragging it. The positional values will be `index`, `x`, and `y`. These values will be used to set the `pointer` on our model.
* `MouseMove Int Int` - This will fire when the mouse moves within the document. If the `pointer` is in `Dragging` state then we'll update the position of the shape being dragged.
* `MouseUp` - This will fire to indicate that we've released the mouse button and are no longer dragging a shape.

So let's modify our `update` function to reflect this logic.

```elm
update : Msg -> Model -> Model
update msg model = 
    case msg of
        MouseDown index x y ->
            { model | pointer = Dragging { index = index, dx = x, dy = y } }
            
        MouseMove x y ->
            case model.pointer of
                Idle ->
                    model
                
                Dragging { index, dx, dy } ->
                    case Array.get index model.shapes of
                        Nothing ->
                            model
                            
                        Just (Circle attributes) ->
                            let
                                shape = Circle 
                                            { attributes 
                                                | cx = x - dx + attributes.cx
                                                , cy = y - dy + attributes.cy
                                            }
                            in
                                { model 
                                    | shapes = Array.set index shape model.shapes 
                                    , pointer = Dragging { index = index, dx = x, dy = y}
                                }
                     
        MouseUp ->
            { model | pointer = Idle }
```

# Drawing shapes
Now we can get to drawing our document. Let's start off by creating a function that
handles rendering a shape.

```elm
shapeView : Int -> Shape -> Svg Msg
shapeView index (Circle attributes) =
    Svg.circle
        [ Attributes.cx 
            <| String.fromInt attributes.cx
        , Attributes.cy 
            <| String.fromInt attributes.cy
        , Attributes.r 
            <| String.fromInt attributes.r
        , Attributes.fill attributes.fill
        , Attributes.stroke "black"
        , Attributes.strokeWidth "2"
        , onMouseDown <| MouseDown index
        ]
        []
```

And then let's update our `view` function to bring it in to the loop.

```elm
view : Model -> Svg Msg
view model =
    Svg.svg 
        [ Attributes.width 
            <| String.fromInt model.document.width
        , Attributes.height 
            <| String.fromInt model.document.height
        , onMouseMove MouseMove
        , Events.onMouseUp MouseUp
        ]
        <| Array.toList 
        <| Array.indexedMap shapeView model.shapes
```


# Putting it all together
