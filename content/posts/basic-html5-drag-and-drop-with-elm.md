Title: Basic HTML5 Drag and Drop with Elm
Category: Blog
Date: 06-18-2018 13:37:00
Series: Practical Elm

In doing some research for a potential project I decided to see how drag and drop 
functionality can be implemented in Elm.

Thankfully, it looks like it's not too hard to achieve since drag and drop is now 
part of the HTML5 standard. To demonstrate this I'll show you how to build an application 
that allows you to construct a list by dragging items onto it.

To follow along with this tutorial I recommend building an application with [Ellie](https://ellie-app.com).

# Getting Started

To get things started we'll start with a `beginnerProgram` since we won't need `init` 
or `subscriptions`.

<!-- https://ellie-app.com/yCv5t7PhHMa1 -->

```elm
import Html exposing (Html)
import Html.Attributes as Attributes


main : Program Never Model Msg
main =
    Html.beginnerProgram
        { model = model
        , update = update
        , view = view
        }


type alias Model =
    { items : List String
    }


model : Model
model = Model []


type Msg 
    = Noop


update : Msg -> Model -> Model
update msg model =
    case msg of
        Noop -> 
            model


view : Model -> Html Msg
view model =
    Html.div
        [ Attributes.class "container" ]
        [ Html.div 
            [ Attributes.class "row" ] 
            [ Html.div 
                [ Attributes.class "col-sm-6" ]
                [ Html.h4 [] [ Html.text "Draggable" ] ]
            , Html.div 
                [ Attributes.class "col-sm-6" ]
                [ Html.h4 [] [ Html.text "Drop Zone" ] ]
            ]
        ]
```

For styling I'm using the [mini.css](https://minicss.org) so you'll want to add the stylesheet for that.

```html
<head>
    <link rel="stylesheet" href="https://unpkg.com/mini.css@3.0.0/dist/mini-default.min.css">
</head>
```

At this point running the application should display the shell that we've setup. Now we can move onto adding 
in the fun stuff.

# Create a list of draggable items

First we need to add a new property to our `Model` for tracking the item that is 
being dragged. I'm also going to add a list of draggable items to the model so that 
we can compose our list of different items. 

<!-- https://ellie-app.com/yCwjh5zF5Ca1 -->

```elm
type alias Model =
    { beingDragged : Maybe String
    , draggableItems: List String
    , items : List String
    }
    
    
model =
    { beingDragged = Nothing
    , draggableItems =
        List.range 1 5
            |> List.map toString
    , items = []
    }
```

Now let's update our `view` to render the draggable items.

<!-- https://ellie-app.com/yCyW9TXhW3a1 -->

```elm
draggableItemView : String -> Html Msg
draggableItemView item =
    Html.div
        [ Attributes.class "card fluid warning"
        ] 
        [ Html.div 
            [ Attributes.class "section" ] 
            [ Html.text item ] 
        ]


itemView : String -> Html Msg
itemView item =
    Html.div
        [ Attributes.class "card fluid error" ] 
        [ Html.div 
            [ Attributes.class "section" ] 
            [ Html.text item ]
        ]


view : Model -> Html Msg
view model =
    Html.div
        [ Attributes.class "container" ]
        [ Html.div 
            [ Attributes.class "row" ] 
            [ Html.div 
                [ Attributes.class "col-sm-6" ]
                <| (List.map draggableItemView model.draggableItems
                    |> (::) (Html.h4 [] [ Html.text "Draggable" ]))
            , Html.div 
                [ Attributes.class "col-sm-6"
                ]
                <| (List.map itemView model.items
                    |> (::) (Html.h4 [] [ Html.text "Drop Zone" ]))
            ]
        ]
```

# Add update messages

Next we need to setup some messages for handling actions in the application. These messages 
will be passed by the event handlers we're going to setup in the next section.

<!-- https://ellie-app.com/yCzmNzPY7ga1 -->

```elm
type Msg
    = Drag String
    | DragEnd
    | DragOver
    | Drop


update : Msg -> Model -> Model
update msg model =
    case msg of
        Drag item ->
            { model | beingDragged = Just item }
            
        DragEnd ->
            { model | beingDragged = Nothing }
            
        DragOver ->
            model
            
        Drop ->
            case model.beingDragged of
                Nothing ->
                    model
                    
                Just item ->
                    { model
                        | beingDragged = Nothing
                        , items = item :: model.items 
                    }
```

# Add event handlers

Next we need to leverage the following events to achieve drag and drop functionality.

Event | Description
--- | ---
`dragstart` | Fires when an element starts being dragged.
`dragend` | Fires when dragging stops without being dropped on a dropzone.
`dragover` | Fires when an dragging over an element. Cancelling this event allows an element to be a dropzone.
`drop` | Fires when dragging stops over a dropzone.

<br>

Handlers for these events aren't provided in `Html.Events`. Thankfully, these are fairly trivial to setup.

<!-- https://ellie-app.com/yCC93bXx2ma1 -->

```elm
import Html.Events as Events
import Json.Decode as Decode


onDragStart msg =
    Events.on "dragstart" 
        <| Decode.succeed msg


onDragEnd msg =
    Events.on "dragend"
        <| Decode.succeed msg


onDragOver msg =
    Events.onWithOptions "dragover"
        { stopPropagation = False
        , preventDefault = True
        }
        <| Decode.succeed msg


onDrop msg =
    Events.onWithOptions "drop"
        { stopPropagation = False
        , preventDefault = True
        }
        <| Decode.succeed msg
```

Then all that's left now is for us to wire up the events in our `view`. Note this 
currently contains a `dataTransfer` hack in order for Firefox to work correctly.

<!-- https://ellie-app.com/yFqTMSKjHQa1 -->

```elm
draggableItemView : String -> Html Msg
draggableItemView item =
    Html.div
        [ Attributes.class "card fluid warning"
        , Attributes.draggable "true"
        , Attributes.attribute "ondragstart"
            "event.dataTransfer.setData(\"text/plain\", \"dummy\")"
        , onDragStart <| Drag item
        , onDragEnd DragEnd 
        ] 
        [ Html.div 
            [ Attributes.class "section" ] 
            [ Html.text item ] 
        ]


itemView : String -> Html Msg
itemView item =
    Html.div
        [ Attributes.class "card fluid error" ] 
        [ Html.div 
            [ Attributes.class "section" ] 
            [ Html.text item ]
        ]


view : Model -> Html Msg
view model =
    Html.div
        [ Attributes.class "container" ]
        [ Html.div 
            [ Attributes.class "row" ] 
            [ Html.div 
                [ Attributes.class "col-sm-6" ]
                <| (List.map draggableItemView model.draggableItems
                    |> (::) (Html.h4 [] [ Html.text "Draggable" ]))
            , Html.div 
                [ Attributes.class "col-sm-6"
                , onDragOver DragOver
                , onDrop Drop
                ]
                <| (List.map itemView model.items
                    |> (::) (Html.h4 [] [ Html.text "Drop Zone" ]))
            ]
        ]
```

# Putting it all together

With everything in place now, you should have a solution like below that allows you to drag 
items from the left list onto the right list.

<iframe src="https://ellie-app.com/embed/yFqTMSKjHQa1" style="width:100%; height:400px; border:0; overflow:hidden;" sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"></iframe>

And that's all it takes to implement basic HTML5 drag and drop in Elm. Happy hacking!