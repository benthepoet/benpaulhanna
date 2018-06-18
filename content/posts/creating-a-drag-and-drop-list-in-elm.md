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
`beginnerProgram` since we won't need `init` or `subscriptions`.

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

First we need to add a new property to our `Model` for tracking the item that is 
being dragged.

```elm
type alias Model =
    { dragged : String
    , items : List String
    }
    
    
model = Model "" []
```