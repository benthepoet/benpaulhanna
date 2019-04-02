Title: Building a 2D Game: Parsing s-expressions in C
Category: Blog
Date: 04-02-2019 11:09:00
Modified: 04-02-2019 11:09:00
Series: Building a 2D Game

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