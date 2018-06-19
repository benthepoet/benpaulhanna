Title: Native HTML5 Drag and Drop with Elm
Category: Blog
Date: 06-18-2018 13:37:00
Series: Practical Elm

In doing some research for a potential project I decided to see how drag and drop 
functionality can be implemented in Elm.

Thankfully, it looks like it's not too hard to achieve since drag and drop is now 
part of the HTML5 standard. To demonstrate this I'll show you how to build an application 
that allows you to construct a list by dragging items onto it.

# Bootstrap the application

To get things started we'll start with a `beginnerProgram` since we won't need `init` 
or `subscriptions`.

https://ellie-app.com/y7qfpb8R7za1

```elm
import Html exposing (Html)
import Html.Events as Events


type alias Model =
    { items : List String
    }


type Msg 
    = Add String


main : Program Never Model Msg
main =
    Html.beginnerProgram
        { model = model
        , update = update
        , view = view
        }


model : Model
model = Model []


update : Msg -> Model -> Model
update msg model =
    case msg of
        Add item -> 
            { model | items = item :: model.items }


itemView : String -> Html Msg
itemView item =
    Html.li [] [ Html.text item ]


view : Model -> Html Msg
view model =
    Html.div [] 
        [ Html.div [] 
            [ Html.button 
                [ Events.onClick <| Add "Item" ] 
                [ Html.text "Add Item"]
            ]
        , Html.ul []
            <| List.map itemView model.items
        ]
```

Right now this application allows you add an element to the `items` list when 
a button is clicked. Let's make some modifications so that instead of clicking the 
button, we drag the item to the list in order to add a new one.

# Re-factor the model

First we need to add a new property to our `Model` for tracking the item that is 
being dragged. I'm also going to add a list of draggable items to the model so that 
we can compose our list of different items. 

https://ellie-app.com/y7qBcZKG2Wa1

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

https://ellie-app.com/y7srmMFyX6a1

```elm
draggableItemView : String -> Html Msg
draggableItemView item =
    Html.li [] [ Html.text item ]


itemView : String -> Html Msg
itemView item =
    Html.li [] [ Html.text item ]


view : Model -> Html Msg
view model =
    Html.div [] 
        [ Html.ul []
            <| List.map draggableItemView model.draggableItems
        , Html.ul []
            <| List.map itemView model.items
        ]
```

# Add event handlers and messages

Next we need to leverage the following events to achieve drag and drop functionality.

##### dragstart
An event that fires when an element starts being dragged. We'll use this event 
to set `beingDragged` on our model.

##### dragend
An event that fires when dragging stops without being droppped on a valid dropzone.

##### dragover
An event that fires when an element enters a potential dropzone. In order to use 
an element as a dropzone we have to prevent the default the behavior for this event. 

##### drop
An event that fires when an elment is released over a valid dropzone. We'll use 
this event to take the value from `beingDragged` and add it to `items`.

Handlers for these aren't provided in `Html.Events` so we'll need to roll our own.

https://ellie-app.com/y98znSNhRpa1

```elm
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

To deal with these events in our `update` function let's change up our message type.

https://ellie-app.com/y9xgkhWJCFa1

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

# Wrapping up

All that's left now is for us to wire up the events in our `view`.

https://ellie-app.com/y9QYcS55WKa1

```elm
import Html.Attributes as Attributes


draggableItemView : String -> Html Msg
draggableItemView item =
    Html.li 
        [ Attributes.draggable "true"
        , onDragStart <| Drag item
        , onDragEnd DragEnd 
        ] 
        [ Html.text item ]


itemView : String -> Html Msg
itemView item =
    Html.li [] [ Html.text item ]


view : Model -> Html Msg
view model =
    Html.div [] 
        [ Html.ul []
            <| List.map draggableItemView model.draggableItems
        , Html.ul 
            [ onDragOver DragOver
            , onDrop Drop
            ]
            <| List.map itemView model.items
        ]
```

And with that you should now be able to drag items into the list as in the application 
below.

https://ellie-app.com/ybztRbFbzZa1

<iframe src="https://ellie-app.com/embed/ybztRbFbzZa1" style="width:100%; height:400px; border:0; overflow:hidden;" sandbox="allow-modals allow-forms allow-popups allow-scripts allow-same-origin"></iframe>