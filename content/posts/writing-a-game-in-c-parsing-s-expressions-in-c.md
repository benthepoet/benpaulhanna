Title: Writing a Game in C: Parsing S-expressions
Category: Blog
Date: 04-03-2019 12:49:00
Modified: 04-03-2019 12:49:00
Series: Writing a Game in C

Over the past couple weeks I've been trying to work out how 
I want to store my game configuration. At first I started playing with XML, which 
was nice because I could stream a file rather than loading the entire thing into memory but
I turned away from XML because I'd rather be as library independent as possible, ideally 
with my SDL being my only cross-platform dependency to worry about.

So for a while I switched my game configuration over to a plain text format that looks like this. This format 
really doesn't have a specific structure to it and I basically mimicked the idea of XML namespaces 
so I could still read it in as a stream and not have to worry about collisions between like named properties. 

```
sp:sprite
  sp:x 32
  sp:y 104
  an:animation
    an:texture "assets/idle.bmp"
    an:frame-length 2
    an:frame-width 24
    an:frame-height 24
    an:frame-span 5
    an:loop 0
```

It felt a little lacking though and over the past few months I've really taken a liking to Common Lisp. 
In the end I really wanted to see my data structured more like this.

```lisp
(:sprites
  ((:sprite
      :x 32
      :y 104
      :animations
        ((:animation
            :texture "assets/idle.bmp"
            :frame-length 2
            :frame-width 24
            :frame-height 24
            :frame-span 5
            :loop 0)))))
```

So I figured I'd stretch my mind and build an s-expression parser. Below is an account of how 
I worked through the solution.

# Modeling the structure 
I'll admit I'm largely a self-taught programmer and don't have a formal background in computer science. Thus, 
I tend to learn about data structures and algorithms when they're useful to a particular problem that I'm trying 
to solve.

With that said, my understanding of how an s-expression is structured led me to implement a linked list. Below is the basic structure.

```c
enum SNodeType {
  LIST,
  STRING,
  SYMBOL
}

struct SNode {
  struct SNode *next;
  enum SNodeType type;
  union {
    struct SNode *list;
    char *value;
  }
}
```

In my program a parsed s-expression is a linked list consisting of `SNode`. The `SNode` struct is a tagged union 
that either contains a value (`STRING` or `SYMBOL` to begin with) or another list of `SNode`. This structure makes for a traversable 
in-memory tree. 

# Recursing the s-expression
So for actually parsing out the expression I decided to utilize `fscanf` as it allows for basic pattern matching.

```c
struct SNode *parse(FILE *fp) {
  struct SNode *tail, *head = NULL;
  char c;
  
  while ((c = fgetc(fp)) != EOF) {
    struct SNode *node = NULL;
    
    if (c == ')') {
      // Stop recursion at the end of an expression
      break;
    } else if (c == '(') {
      // Begin recursion at the start of an expression
      node = calloc(1, sizeof(struct SNode));
      node->type = LIST;
      node->list = parse(fp);
    } else if (!isspace(c)) {
      ungetc(c, fp);
      
      char buffer[512];
      
      if (c == '"') {
        // Read a string terminated by double quote
        if (fscanf(fp, "\"%511[^\"]\"", buffer)) {
          node = calloc(strlen(buffer) + 1, sizeof(struct SNode));
          node->type = STRING;
          strcpy(node->value, buffer);
        }
      } else {
        // Read a symbol terminated by whitespace or parentheses
        if (fscanf(fp, "%511[^()\t\r\n\v\f ]", buffer)) {
          node = calloc(strlen(buffer) + 1, sizeof(struct SNode));
          node->type = SYMBOL;
          strcpy(node->value, buffer);
        }
      }
    }
    
    // Append a node
    if (node != NULL) {
      if (head == NULL) {
        // Initialize the head
        head = tail = node;
      } else {
        // Append the node to the tail
        tail = tail->next = node;
      }
    }
  }
  
  // Return the head of the list
  return head;
}
```

This worked fairly well. I did however notice later on that this iteration of the parser couldn't read empty strings correctly. I also 
wanted to introduce the `FLOAT` and `INTEGER` data types as these currently just get tagged as `SYMBOL`.

# Adding number data types
For basic number support I added `FLOAT` and `INTEGER` to the `SNodeType` enumeration.

```c
enum SNodeType {
  LIST,
  FLOAT,
  INTEGER,
  STRING,
  SYMBOL
}
```

Next I created a couple functions for determining whether a string is a float or an integer.

```c
int is_float(char *str) {
  char *ptr = NULL;
  strtod(str, &ptr);
  return !*ptr;
}

int is_integer(char *str) {
  char *ptr = NULL;
  strtol(str, &ptr, 10);
  return !*ptr;
}
```

I then updated the `parse` function to try and determine the type before falling back to a `SYMBOL`.

```c
// Read a symbol terminated by whitespace or parentheses
if (fscanf(fp, "%511[^()\t\r\n\v\f ]", buffer)) {
  node = calloc(strlen(buffer) + 1, sizeof(struct SNode));
  strcpy(node->value, buffer);

  if (is_integer(node->value)) {
    node->type = INTEGER;
  } else if (is_float(node->value)) {
    node->type = FLOAT;
  } else {
    node->type = SYMBOL;
  }
}
```

After that the parser was able to successfully tag number types. The value itself is still stored as a string though as 
I figured the game should be responsible for handling that conversion.

# Fixing the empty string issue
Even though I'm never expecting my game to read an empty string in from an s-expression, I didn't want that to be a limitation 
of the parser. To fix that issue meant I was going to have to abandon `fscanf`. The limitation of using `fscanf` for 
reading strings is that its format pattern expects there to be at least one character between the quotes. With the case of the 
empty string, there's nothing in between the quotes for it to capture so it winds up parsing the rest of expression incorrectly.

The solution I came up with in the end is a little longer but it probably performs better than `fscanf`.

```c
} else if (c == '"') {
  int length = 0;
  char buffer[512];

  // Read until string terminator
  while ((c = fgetc(fp)) != '"' && length < 511) {
    buffer[length] = c;
    length++;
  }
  buffer[length] = '\0';

  node = calloc(1, sizeof(struct SNode));
  node->type = STRING;
  node->value = calloc(length + 1, sizeof(char));
  strcpy(node->value, buffer);
}
```

To stay consistent with this means of parsing I also updated the logic for parsing numbers and symbols. One key issue I found with when 
doing this was that I had to remember to put the terminator back, otherwise the parser wouldn't close the current list and subsequent symbols 
would wind up in the wrong list.

```c
} else if (!isspace(c)) {
  int length = 1;
  char buffer[512] = { c };

  // Read until whitespace or list terminator
  while (!is_terminator(c = fgetc(fp)) && length < 511) {
    buffer[length] = c;
    length++;
  }
  buffer[length] = '\0';

  // Put the terminator back
  ungetc(c, fp);

  node = calloc(1, sizeof(struct SNode));
  node->value = calloc(length + 1, sizeof(char));
  strcpy(node->value, buffer);

  if (is_integer(node->value)) {
    node->type = INTEGER;
  } else if (is_float(node->value)) {
    node->type = FLOAT;
  } else {
    node->type = SYMBOL;
  }
}
```

With those changes made, the `parse` function is now fairly robust in its current form.

```c
// Recursively parse an s-expression from a file stream
struct SNode *parse_sexpr_file(FILE *fp) {
  // Using a linked list, nodes are appended to the list tail until we 
  // reach a list terminator at which point we return the list head.
  struct SNode *tail, *head = NULL;
  int c;

  while ((c = fgetc(fp)) != EOF) {
    struct SNode *node = NULL;

    if (c == ')') {
      // Terminate list recursion
      break;
    } else if (c == '(') {
      // Begin list recursion
      node = calloc(1, sizeof(struct SNode));
      node->type = LIST;
      node->list = parse_sexpr_file(fp);
    } else if (c == '"') {
      int length = 0;
      char buffer[BUFFER_SIZE];

      // Read until string terminator
      while ((c = fgetc(fp)) != '"' && length < BUFFER_SIZE - 1) {
        buffer[length] = c;
        length++;
      }
      buffer[length] = '\0';

      node = calloc(1, sizeof(struct SNode));
      node->type = STRING;
      node->value = calloc(length + 1, sizeof(char));
      strcpy(node->value, buffer);
    } else if (!isspace(c)) {
      int length = 1;
      char buffer[BUFFER_SIZE] = { c };

      // Read until whitespace or list terminator
      while (!is_terminator(c = fgetc(fp)) && length < BUFFER_SIZE - 1) {
        buffer[length] = c;
        length++;
      }
      buffer[length] = '\0';
      
      // Put the terminator back
      ungetc(c, fp);

      node = calloc(1, sizeof(struct SNode));
      node->value = calloc(length + 1, sizeof(char));
      strcpy(node->value, buffer);

      if (is_integer(node->value)) {
        node->type = INTEGER;
      } else if (is_float(node->value)) {
        node->type = FLOAT;
      } else {
        node->type = SYMBOL;
      }
    }

    if (node != NULL) {
      if (head == NULL) {
        // Initialize the list head
        head = tail = node;
      } else {
        // Append the node to the list tail
        tail = tail->next = node;
      }
    }
  }

  return head;
}
```

# Deallocating memory
The last thing I needed to do is write a recursive function for freeing the memory that is dynamically 
allocated by the `SNode` tree. This is how that looks.

```c
// Recursively free memory allocated by a node
void snode_free(struct SNode *node) {
  struct SNode *tmp;

  while (node != NULL) {
    tmp = node;

    if (node->type == LIST) {
      snode_free(node->list);
    } else {
      // Free current value
      free(node->value);
      node->value = NULL;
    }

    node = node->next;

    // Free current node
    free(tmp);
    tmp = NULL;
  }
}
```

# Wrapping up
In the end I'm really satisfied with how the parser turned out and I dissassembled the 
solution down to a level where I could easily implement it in other languages if I need 
to (or I'm just bored). If you'd like to use or fork the parser then please 
see my [c-sexpr-parser](https://github.com/benthepoet/c-sexpr-parser) repository.